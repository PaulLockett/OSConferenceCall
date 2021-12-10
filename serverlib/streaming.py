"""
This module implements the main functionality of vidstream.

Author: Florian Dedov from NeuralNine
YouTube: https://www.youtube.com/c/NeuralNine
"""

__author__ = "Florian Dedov, NeuralNine"
__email__ = "mail@neuralnine.com"
__status__ = "planning"

import cv2
import pyautogui
import numpy as np

import socket
import pickle
import struct
import threading


class StreamingServer:
    """
    Class for the streaming server.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening
        __clients : list
            list of all connected clients
        __used_slots : int
            amount of used slots (not ready yet)
        __quit_key : chr
            key that has to be pressed to close connection
        __running : bool
            inicates if the server is already running or not
        __block : Lock
            a basic lock used for the synchronization of threads
        __server_socket : socket
            the main server socket


    Methods
    -------

    Private:

        __init_socket : method that binds the server socket to the host and port
        __server_listening: method that listens for new connections
        __client_connection : main method for processing the client streams

    Public:

        start_server : starts the server in a new thread
        stop_server : stops the server and closes all connections
    """

    def __init__(self, host, port, quit_key='q'):
        """
        Creates a new instance of StreamingServer

        Parameters
        ----------

        host : str
            host address of the listening server
        port : int
            port on which the server is listening
        slots : int
            amount of avaialable slots (not ready yet) (default = 8)
        quit_key : chr
            key that has to be pressed to close connection (default = 'q')  
        """
        self.__host = host
        self.__port = port
        self.__clients = []
        self.__used_slots = 0
        self.__running = False
        self.__quit_key = quit_key
        self.__block = threading.Lock()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init_socket()

    def __init_socket(self):
        """
        Binds the server socket to the given host and port
        """
        self.__server_socket.bind((self.__host, self.__port))

    def start_server(self):
        """
        Starts the server if it is not running already.
        """
        if self.__running:
            print("Server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()
            print("Server started")

    def __server_listening(self):
        """
        Listens for new connections.
        """
        self.__server_socket.listen()
        while self.__running:

            client_socket, _ = self.__server_socket.accept()
            self.__clients.append(client_socket)

            thread = threading.Thread(target=self.__client_connection, args=(client_socket,))
            thread.start()
            print("server: new client connected")

    def stop_server(self):
        """
        Stops the server and closes all connections
        """
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
            print("Server stopped")
        else:
            print("Server not running!")

    def __client_connection(self, client_socket):
        """
        Handles the individual client connections and processes their stream data.
        """

        while self.__running:
            try:
                received = client_socket.recv(4096)
                if received == b'':
                    break
                
                for client in self.__clients:
                    client.sendall(received)
            except:
                self.__clients.remove(client_socket)
                client_socket.close()
                print("server: a client disconnected from server")
                break
                    
                    
class StreamingClient:
    """
    class for the camera streaming and listening client.

    Attributes
    ----------

    Private:

        __host : str
            host address to connect to
        __port : int
            port to connect to
        __running : bool
            inicates if the client is already listening or not
        __streaming : bool
            inicates if the client is already streaming or not
        __encoding_parameters : list
            a list of encoding parameters for OpenCV
        __client_socket : socket
            the main client socket
        __camera : VideoCapture
            the camera object
        __x_res : int
            the x resolution
        __y_res : int
            the y resolution
        __quit_key : chr
            key that has to be pressed to close connection


    Methods
    -------

    Private:

        __client_streaming : main method for streaming the client data
        __server_listening : main method for listening for server data

    Protected:

        _configure : sets basic configurations
        _get_frame : returns the camera frame to be sent to the server
        _cleanup : cleans up all the resources and closes everything

    Public:

        start_streaming : starts the camera stream in a new thread
        start_listening : starts the server listener in a new thread
        stop_streaming : stops the camera stream
        disconnect : disconnects from the server
    """

    def __init__(self, host, port, x_res=1024, y_res=576, quit_key='q'):
        """
        Creates a new instance of StreamingClient.

        Parameters
        ----------

        host : str
            host address to connect to
        port : int
            port to connect to
        x_res : int
            x resolution of the stream
        y_res : int
            y resolution of the stream
        quit_key : chr
            key that has to be pressed to close connection (default = 'q')
        """
        self.__host = host
        self.__port = port
        self.__x_res = x_res
        self.__y_res = y_res
        self.__quit_key = quit_key
        self.__camera = cv2.VideoCapture(0)
        self._configure()
        self.__running = False
        self.__streaming = False
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        """
        Sets the camera resultion and the encoding parameters.
        """
        self.__camera.set(3, self.__x_res)
        self.__camera.set(4, self.__y_res)
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        """
        Gets the next camera frame.

        Returns
        -------

        frame : the next camera frame to be processed
        """
        ret, frame = self.__camera.read()
        return frame

    def _cleanup(self):
        """
        Cleans up resources and closes everything.
        """
        self.__camera.release()
        cv2.destroyAllWindows()
        
    def __client_streaming(self, connection):
        """
        Main method for streaming the client data.
        """
        
        while self.__streaming:
            frame = self._get_frame()
            result, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                connection.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__streaming = False
            except ConnectionAbortedError:
                self.__streaming = False
            except BrokenPipeError:
                self.__streaming = False

        self._cleanup()

    def __server_listening(self, connection, address):
        """
        Handles the individual client connections and processes their stream data.
        """
        payload_size = struct.calcsize('>L')
        data = b""

        while self.__running:

            break_loop = False

            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    self.__used_slots -= 1
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(address), frame)
            if cv2.waitKey(1) == ord(self.__quit_key):
                connection.close()
                self.__used_slots -= 1
                break

    def start_listening(self):
        """
        Starts client stream if it is not already running.
        """

        if self.__running:
            print("Client is already connected!")
        else:
            self.__running = True

            self.__client_socket.connect((self.__host, self.__port))

            address = self.__client_socket.getsockname()

            listening_thread = threading.Thread(target=self.__server_listening, args=(self.__client_socket, address,))
            listening_thread.start()
            print("Client is now connected to {}:{}".format(self.__host, self.__port))

    def start_streaming(self):
        """
        Starts the client stream in a new thread.
        """
        if self.__streaming:
            print("Client is already streaming!")
        else:
            self.__streaming = True
            thread = threading.Thread(target=self.__client_streaming, args=(self.__client_socket,))
            thread.start()
            print("Client is now streaming!")

    def stop_stream(self):
        """
        Stops client stream if running
        """
        if self.__streaming:
            self.__streaming = False
            print("Client is now stopped streaming!")
        else:
            print("Client not streaming!")

    def disconnect(self):
        """
        Disconnects the client from the server.
        """
        if self.__running:
            self.__running = False
            self.__client_socket.close()
            print("Client is now disconnected!")
        else:
            print("Client not connected!")
    