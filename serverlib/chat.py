import socket
import threading

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.clients = []
        self.lock = threading.Lock()

    def broadcast(self, message):
        for c in self.clients:
            c.send(message)

    def handle(self, client, address):
        print(f'Connection from {address}')
        while True:
            try:
                data = client.recv(1024)
                if data:
                    self.broadcast(data)
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                self.lock.acquire()
                self.clients.remove(client)
                self.lock.release()
                print(f'Client {address} disconnected')
                break

    def start(self):
        while True:
            client, address = self.sock.accept()
            self.lock.acquire()
            self.clients.append(client)
            self.lock.release()
            threading.Thread(target=self.handle, args=(client, address)).start()
            print(f'Client {address} connected')
    
    def stop(self):
        self.sock.close()
        for c in self.clients:
            c.close()
        print('Chat Server stopped')

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, message):
        self.sock.send(message)

    def receive(self):
        return self.sock.recv(1024)

    def close(self):
        self.sock.close()