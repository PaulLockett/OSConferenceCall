import socket
import pyaudio
import threading
class AudioClient:

    def __init__(self, host, port, audio_format=pyaudio.paInt16, channels=1, rate=44100, frame_chunk=4096):
        self.__host = host
        self.__port = port

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__audio = pyaudio.PyAudio()

        self.__running = False
        self.__streaming = False
       
    def start_stream(self):
        if self.__streaming:
            print("Already streaming")
        else:
            self.__streaming = True
            thread = threading.Thread(target=self.__audio_streaming)
            thread.start()
            print("Streaming audio")
    
    def stop_stream(self):
        if self.__streaming:
            self.__streaming = False
            print("Stopped streaming")
        else:
            print("Client already not streaming")
    
    def __audio_streaming(self):
        while self.__streaming:
            self.__client_socket.send(self.__streamIn.read(self.__frame_chunk))
    
    def __audio_connection(self):
        while self.__running:
            data = self.__client_socket.recv(self.__frame_chunk)
            self.__streamOut.write(data)
    
    def start_listening(self):
        """
        Starts client audio stream if it is not already running.
        """

        if self.__running:
            print("(Audio)Client is already connected!")
        else:
            self.__running = True

            self.__client_socket.connect((self.__host, self.__port))
            self.__streamOut = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, output=True, frames_per_buffer=self.__frame_chunk)
            self.__streamIn = self.__audio.open(format=self.__audio_format, channels=self.__channels, rate=self.__rate, input=True, frames_per_buffer=self.__frame_chunk)
            thread = threading.Thread(target=self.__audio_connection)
            thread.start()

            print("(Audio)Client is now connected to {}:{}".format(self.__host, self.__port))
        
    def disconnect(self):
        """
        Disconnects client from server.
        """

        if self.__running:
            self.__running = False
            self.__streamIn.stop_stream()
            self.__streamIn.close()
            self.__streamOut.stop_stream()
            self.__streamOut.close()
            self.__client_socket.close()
            self.__audio.terminate()
            print("(Audio)Client is now disconnected")
        else:
            print("(Audio)Client is not connected")

class AudioServer:

    def __init__(self, host, port, audio_format=pyaudio.paInt16, channels=1, rate=44100, frame_chunk=4096):
        self.__host = host
        self.__port = port

        self.__clients = []

        self.__audio_format = audio_format
        self.__channels = channels
        self.__rate = rate
        self.__frame_chunk = frame_chunk

        self.__audio = pyaudio.PyAudio()

        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server_socket.bind((self.__host, self.__port))

        self.__block = threading.Lock()
        self.__running = False

    def start_server(self):
        if self.__running:
            print("Audio server is running already")
        else:
            self.__running = True
            thread = threading.Thread(target=self.__server_listening)
            thread.start()

    def __server_listening(self):
        self.__server_socket.listen()
        while self.__running:
            client_socket, _ = self.__server_socket.accept()
            self.__clients.append(client_socket)

            thread = threading.Thread(target=self.__brodcast_audio, args=(client_socket,))
            thread.start()
            print("server: new (Audio)client connected")

    def __brodcast_audio(self, client_socket):

        while self.__running:
            try:
                data = client_socket.recv(self.__frame_chunk)

                for client in self.__clients:
                    client.send(data)
            except:
                self.__clients.remove(client_socket)
                client_socket.close()
                print("server: a (Audio) client disconnected from server")
                break

    def stop_server(self):
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
            print("(Audio)Server is now closed")
        else:
            print("Server not running!")