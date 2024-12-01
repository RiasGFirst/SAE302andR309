from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox
from PyQt6.QtCore import Qt
import threading
import socket
import time
import sys


# create the class for the connection to the server
class ServerConnection:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__client_socket = None

    def connect(self):
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__client_socket.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            print("Connection refused")
            return
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        else:
            self.__authenticate()


    def __authenticate(self):
        self.__client_socket.send("<CLIENT_AUTH>".encode())
        if self.__client_socket.recv(1024).decode() == "<SEND_CLIENT_ID>":
            self.__client_socket.send("client".encode())
            time.sleep(0.5)
            self.__client_socket.send(self.__username.encode())
            time.sleep(0.5)
            self.__client_socket.send(self.__password.encode())
            msg = self.__client_socket.recv(1024).decode()
            if msg == "<CLIENT_AUTH_SUCCESS>":
                print(f"Client authenticated with id: {self.__username}")

                auth_send = self.__client_socket.recv(1024).decode()

                if auth_send == "<SEND_CLIENT_DATA>":
                    self.__client_socket.send(f"I'm {self.__username}".encode())
                    time.sleep(1)
                    self.__client_socket.send("Hello World!".encode())
                    time.sleep(60)
                    self.__client_socket.send("<CLIENT_QUIT>".encode())
                    self.__client_socket.close()
                elif auth_send == "<CLIENT_EXCEEDED>":
                    msg = self.__client_socket.recv(1024).decode()
                    time.sleep(0.5)
                    if msg == "<SERVER_AVAILABLE>":
                        data = self.__client_socket.recv(1024).decode()
                        print(f"Please login on {data}")
                        self.__client_socket.close()
                    else:
                        print("No server available")
                        self.__client_socket.close()
                else:
                    print("We don't want to connect to the server :)")
                    self.__client_socket.close()
            elif msg == "<CLIENT_ALREADY_CONNECTED>":
                print("Client already connected")
                self.__client_socket.close()
            elif msg == "<CLIENT_AUTH_FAILED>":
                print("Authentication failed")
                self.__client_socket.close()
            else:
                print("We don't want to connect to the server :)")
                self.__client_socket.close()

        else:
            print("Authentication failed")
            self.__client_socket.close()


    def send_file(self, file_path: str):
        pass



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload'R")
        self.setMinimumSize(700, 700)

        # Section: Connexion
        self.connection_group = QGroupBox("Connexion")
        connection_layout = QGridLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()

        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connectToServer)

        connection_layout.addWidget(self.username_label, 0, 0)
        connection_layout.addWidget(self.username_input, 0, 1)
        connection_layout.addWidget(self.password_label, 0, 2)
        connection_layout.addWidget(self.password_input, 0, 3)
        connection_layout.addWidget(self.host_label, 0, 4)
        connection_layout.addWidget(self.host_input, 0, 5)
        connection_layout.addWidget(self.port_label, 0, 6)
        connection_layout.addWidget(self.port_input, 0, 7)
        connection_layout.addWidget(self.connect_button, 0, 8)

        self.connection_group.setLayout(connection_layout)

        # Section: Envoi de fichiers
        self.file_group = QGroupBox("Envoi de fichiers")
        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Chemin du fichier à envoyer...")
        self.send_button = QPushButton("Envoyer")

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.send_button)
        self.file_group.setLayout(file_layout)

        # Section: Console
        self.console_group = QGroupBox("Console")
        console_layout = QVBoxLayout()

        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)

        console_layout.addWidget(self.console_output)
        self.console_group.setLayout(console_layout)

        # Organisation principale
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.connection_group)
        main_layout.addWidget(self.file_group)
        main_layout.addWidget(self.console_group)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def connectToServer(self):
        username = self.username_input.text()
        password = self.password_input.text()
        host = self.host_input.text()
        port = int(self.port_input.text())

        serverConn = ServerConnection(host, port, username, password)
        serverConn.connect()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
