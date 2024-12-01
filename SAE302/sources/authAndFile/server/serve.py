import utils.check_compilor as check_compilor
import utils.file_services as file_services
import utils.auth as auth
import threading
import argparse
import socket
import time


def reception_message(client_socket):
    global client_connected
    client_type = None
    client_id = None
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except (ConnectionResetError, ConnectionAbortedError):
            print(f"\033[31m[*] {client_type} {client_id} has left the chat\033[0m")
            client_socket.close()
            return
        else:
            if client_type == "client" and client_id is not None:
                if message == "<CLIENT_QUIT>":
                    client_socket.send("<CLIENT_DISCONNECT>".encode())
                    time.sleep(1)
                    client_connected.remove(client_id)
                    print(f"\033[31m[*] {client_type} {client_id} has left the chat\033[0m")
                    client_socket.close()
                    return
                if message == "<CLIENT_FILE_SERVICE>":
                    file_services.file_services(client_socket, client_id)
                else:
                    pass
            else:
                if message == "<CLIENT_AUTH>":
                    client_type, client_id = auth.authentificate(client_socket, client_connected)
                    if client_type is None or client_id is None:
                        client_socket.close()
                        return
                else:
                    client_socket.send("<CLIENT_AUTH>".encode())


def serve(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', port))
    except OSError:
        print(f"\033[31m[*] Port {port} already opened!\033[0m")
        server.close()
        return

    server.listen(5)
    print(f"\033[32m[*] Listening on {server.getsockname()} \033[0m")

    while True:
        try:
            client, addr = server.accept()
            print(f"\033[31m[*] Accepted connection from {addr}\033[0m")
            # Création d'un nouveau thread pour gérer le client
            tlisten = threading.Thread(target=reception_message, args=(client,))
            tlisten.daemon = True  # Permet de fermer les threads en même temps que le programme principal
            tlisten.start()
        except KeyboardInterrupt:
            print("\n\033[31m[*] Server shutting down...\033[0m")
            server.close()
            break


if __name__ == "__main__":
    client_connected = []
    # Creer des arguments pour le port
    parser = argparse.ArgumentParser(description="Servers")
    parser.add_argument("-p", "--port", type=int, help="Port d'écoute du serveur", default=9990)
    args = parser.parse_args()
    compilateurs = {
        "C": "gcc",
        "C++": "g++",
        "Java": "javac",
        "Python": "python"
    }
    check_compilor.verify_compile(compilateurs)
    serve(args.port)