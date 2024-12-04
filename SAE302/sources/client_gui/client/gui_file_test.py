from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QGroupBox, QFileDialog
from PyQt6.QtCore import Qt
import threading
import socket
import time
import sys
import os

client_socket = None
is_connected = False

def listen_to_server(console_output):
    global is_connected, client_socket
    try:
        while is_connected:
            msg = client_socket.recv(1024).decode()
            if msg == "<CLIENT_DISCONNECT>":
                log_to_console("En cours de déconnexion...", console_output)
                time.sleep(1)
                log_to_console("Déconnecté du serveur", console_output)
                is_connected = False
            else:
                if msg == "":
                    pass
                else:
                    log_to_console(f"Serveur : {msg}", console_output)
    except Exception as e:
        print(f"Erreur : {e}")
        is_connected = False
    finally:
        client_socket.close()


def log_to_console(msg, console_output):
    console_output.append(msg)


def server_connection(host, port, username, password, console_output):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        client_socket.send("<CLIENT_AUTH>".encode())
        if client_socket.recv(1024).decode() == "<SEND_CLIENT_ID>":
            client_socket.send("client".encode())
            time.sleep(0.5)
            client_socket.send(username.encode())
            time.sleep(0.5)
            client_socket.send(password.encode())
            msg = client_socket.recv(1024).decode()
            if msg == "<CLIENT_AUTH_SUCCESS>":
                log_to_console(f"Authentifié en tant que {username}", console_output)

                auth_send = client_socket.recv(1024).decode()
                if auth_send == "<SEND_CLIENT_DATA>":
                    is_connected = True
                    log_to_console("You can now send your program :)", console_output)
                    threading.Thread(target=listen_to_server, daemon=True, args=(console_output, )).start()
                elif auth_send == "<CLIENT_EXCEEDED>":
                    msg = client_socket.recv(1024).decode()
                    time.sleep(0.5)
                    if msg == "<SERVER_AVAILABLE>":
                        data = client_socket.recv(1024).decode()
                        log_to_console(f"Please login on {data}", console_output)
                        client_socket.close()
                    else:
                        log_to_console("No server available :(", console_output)
                        client_socket.close()
                else:
                    print("We don't want to connect to the server :)")
                    client_socket.close()
            elif msg == "<CLIENT_ALREADY_CONNECTED>":
                log_to_console("Client already connected in another session", console_output)
                client_socket.close()
            elif msg == "<CLIENT_AUTH_FAILED>":
                log_to_console("Authentication failed", console_output)
                client_socket.close()
            else:
                log_to_console("We don't want to connect to the server :)", console_output)
                client_socket.close()
        else:
            log_to_console("Échec de l'authentification", console_output)
            client_socket.close()
    except Exception as e:
        log_to_console(f"Erreur lors de l'authentification : {e}")
        client_socket.close()


def send_file(file_path, console_output):
    global client_socket
    print(client_socket)
    print(file_path)
    file_name = file_path.split("/")[-1]
    file_size = os.path.getsize(file_path)
    print(file_name, file_size)
    try:
        client_socket.send("<CLIENT_FILE>".encode())
        msg = client_socket.recv(1024).decode()
        if msg == "<FILE_SERVICE>":
            msg = client_socket.recv(1024).decode()
            if msg == "<FILE_DATA_REQUESTS>":
                client_socket.send(file_name.encode())
                time.sleep(0.5)
                client_socket.send(str(file_size).encode())
                time.sleep(0.5)
                msg = client_socket.recv(1024).decode()
                if msg == "<FILE_DATA_READY>":
                    file = open(file_path, "rb")
                    data = file.read(1024)
                    client_socket.sendall(data)
                    client_socket.send(b"<FILE_DONE>")
                    file.close()
                    msg = client_socket.recv(1024).decode()
                    if msg == "<FILE_RECEIVED>":
                        log_to_console(f"File {file_name} sent successfully", console_output)
                    else:
                        log_to_console(f"Failed to send file {file_name}", console_output)
                else:
                    log_to_console("Failed to send file", console_output)
    except Exception as e:
        log_to_console(f"Error while sending file : {e}", console_output)





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Upload'R")
        self.setMinimumSize(700, 700)

        # Section : Connexion
        self.connection_group = QGroupBox("Connexion")
        connection_layout = QGridLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setText("rias")

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.host_label = QLabel("Host:")
        self.host_input = QLineEdit()
        self.host_input.setText("127.0.0.1")

        self.port_label = QLabel("Port:")
        self.port_input = QLineEdit()
        self.port_input.setText("9999")

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


        self.select_file_button = QPushButton("Sélectionner un fichier")
        self.select_file_button.clicked.connect(self.selectFile)

        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.sendFile)

        self.file_group = QGroupBox("Fichier")
        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)

        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.select_file_button)
        file_layout.addWidget(self.send_button)
        self.file_group.setLayout(file_layout)

        # Section : Console
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

        server_connection(host, port, username, password, self.console_output)

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*)")
        if file_path:
            self.file_input.setText(file_path)

    def sendFile(self):
        file_path = self.file_input.text()
        if file_path:
            send_file(file_path, self.console_output)
        else:
            self.console_output.append("Veuillez sélectionner un fichier à envoyer")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())