from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, \
    QHBoxLayout, QGridLayout, QGroupBox, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import threading
import socket
import time
import sys
import os
from datetime import datetime

client_socket = None
is_connected = False
lock = threading.Lock()


def log_to_console(msg, console_output):
    """Ajoute un message avec un timestamp à la console."""
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    console_output.append(f"{timestamp} {msg}")


def listen_to_server(console_output):
    """Écoute le serveur et affiche les messages reçus."""
    global is_connected, client_socket
    try:
        while is_connected:
            msg = client_socket.recv(1024).decode()
            if not msg:
                log_to_console("Connexion interrompue par le serveur.", console_output)
                with lock:
                    is_connected = False
                break
            elif msg == "<CLIENT_DISCONNECT>":
                log_to_console("Déconnecté du serveur.", console_output)
                with lock:
                    is_connected = False
                break
            else:
                log_to_console(f"Serveur : {msg}", console_output)
    except Exception as e:
        log_to_console(f"Erreur : {e}", console_output)
    finally:
        client_socket.close()


def server_connection(host, port, username, password, console_output):
    """Établit la connexion avec le serveur."""
    global client_socket, is_connected
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
                with lock:
                    is_connected = True
                threading.Thread(target=listen_to_server, daemon=True, args=(console_output,)).start()
            elif msg == "<CLIENT_ALREADY_CONNECTED>":
                log_to_console("Client déjà connecté.", console_output)
            elif msg == "<CLIENT_AUTH_FAILED>":
                log_to_console("Échec de l'authentification.", console_output)
            else:
                log_to_console("Connexion refusée par le serveur.", console_output)
    except Exception as e:
        log_to_console(f"Erreur lors de la connexion : {e}", console_output)
        if client_socket:
            client_socket.close()
    finally:
        if not is_connected and client_socket:
            client_socket.close()


def send_file(file_path, console_output):
    """Envoie un fichier au serveur."""
    global client_socket
    if client_socket is None or not is_connected:
        log_to_console("Connexion au serveur requise avant d'envoyer un fichier.", console_output)
        return

    if not os.path.isfile(file_path):
        log_to_console("Fichier non valide ou introuvable.", console_output)
        return

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    log_to_console(f"Envoi du fichier : {file_name} ({file_size} octets)", console_output)

    try:
        client_socket.send("<CLIENT_FILE>".encode())
        if client_socket.recv(1024).decode() == "<FILE_SERVICE>":
            client_socket.send(file_name.encode())
            time.sleep(0.5)
            client_socket.send(str(file_size).encode())
            time.sleep(0.5)
            if client_socket.recv(1024).decode() == "<FILE_DATA_READY>":
                with open(file_path, "rb") as file:
                    while chunk := file.read(1024):
                        client_socket.sendall(chunk)
                client_socket.send(b"<FILE_DONE>")
                if client_socket.recv(1024).decode() == "<FILE_RECEIVED>":
                    log_to_console(f"Fichier {file_name} envoyé avec succès.", console_output)
                else:
                    log_to_console(f"Échec de l'envoi du fichier {file_name}.", console_output)
    except Exception as e:
        log_to_console(f"Erreur lors de l'envoi du fichier : {e}", console_output)


class ServerThread(QThread):
    """Thread pour la connexion au serveur."""
    log_signal = pyqtSignal(str)

    def __init__(self, host, port, username, password):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def run(self):
        server_connection(self.host, self.port, self.username, self.password, self.log_signal)


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

        # Section : Fichier
        self.file_group = QGroupBox("Fichier")
        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setReadOnly(True)

        self.select_file_button = QPushButton("Sélectionner un fichier")
        self.select_file_button.clicked.connect(self.selectFile)

        self.send_button = QPushButton("Envoyer")
        self.send_button.clicked.connect(self.sendFile)

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

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def connectToServer(self):
        host = self.host_input.text()
        port = self.port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not host or not port.isdigit() or not username or not password:
            self.console_output.append("Veuillez remplir tous les champs correctement.")
            return

        port = int(port)
        thread = ServerThread(host, port, username, password)
        thread.log_signal.connect(self.console_output.append)
        thread.start()

    def selectFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier", "", "Tous les fichiers (*)")
        if file_path:
            self.file_input.setText(file_path)

    def sendFile(self):
        file_path = self.file_input.text()
        if file_path:
            send_file(file_path, self.console_output)
        else:
            self.console_output.append("Veuillez sélectionner un fichier à envoyer.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
