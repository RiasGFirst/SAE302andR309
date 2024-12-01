import socket
import threading

def handle_client(client_socket, server_socket):
    pass

def envoie_message(client_socket):
    while True:
        try:
            message = input()
        except EOFError:
            return
        try:
            client_socket.send(message.encode())
        except ConnectionResetError:
            return
        except OSError:
            return

def reception_message(client_socket, server_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
        except ConnectionResetError:
            print(f"Le client a fermé la connexion!")
            client_socket.close()
            return
        except ConnectionAbortedError:
            client_socket.close()
            return
        else:
            print(f"{message}")
            if message == "bye":
                print("Le client ferme la connexion")
                reply = "bye"
                client_socket.send(reply.encode())
                client_socket.close()
                return
            elif message == "arret":
                print("Le client a arrêté le serveur")
                reply = "arret"
                client_socket.send(reply.encode())
                client_socket.close()
                server_socket.close()
                return True
            else:
                reply = ""
                try:
                    client_socket.send(reply.encode())
                except OSError:
                    return True
    pass

def main(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind(('0.0.0.0', port))
    except OSError:
        print(f"\033[31mLe port {port} est déjà ouvert!\033[0m")
        server.close()
        return

    server.listen(5)
    print(f"[*] Listening on {server.getsockname()}")
    while True:
        try:
            client, addr = server.accept()
            print(f"[*] Accepted connection from {addr}")
            tlisten = threading.Thread(target=reception_message, args=(client, server))
            twrite = threading.Thread(target=envoie_message, args=(client,))
            tlisten.start()
            twrite.start()
            tlisten.join()
        except OSError:
            return


if __name__ == "__main__":
    main(port=9990)
