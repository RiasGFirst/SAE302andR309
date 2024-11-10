import socket
import threading

class Server:

    def __init__(self, name, port=5000, clientmax=2):
        self.__name = name
        self.__port = port
        self.__clientmax = clientmax
        self.clients = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def clientmax(self):
        return self.__clientmax

    @clientmax.setter
    def clientmax(self, clientmax):
        self.__clientmax = clientmax

    def __str__(self):
        return f"Server: {self.__name} on port {self.__port}"

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")
        self.clients.append(client_socket)
        try:
            while True:
                # Example of receiving data from the client
                data = client_socket.recv(1024)
                if not data:
                    break
                print(f"Received from {address}: {data.decode()}")
                # Example response to client
                client_socket.send("Acknowledged".encode())
        except Exception as e:
            print(f"Error with client {address}: {e}")
        finally:
            print(f"Connection with {address} closed")
            client_socket.close()
            self.clients.remove(client_socket)

    def run_serve(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((socket.gethostname(), self.__port))
        server.listen(self.__clientmax)
        print(f"Server {self.__name} is running on {socket.gethostname()}:{self.__port}")

        while True:
            if len(self.clients) < self.__clientmax:
                client_socket, address = server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                client_thread.start()
            else:
                print("Maximum client limit reached. Waiting for a client to disconnect.")
                continue