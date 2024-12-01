import socket
import threading


def send_msg(client_socket):
    while True:
        message = ""
        while message == "":
            try:
                message = input()
            except EOFError:
                return
        try:
            client_socket.send(message.encode())
        except ConnectionResetError:
            print(f"\033[31mLe serveur a fermé la connexion!\033[0m")
            client_socket.close()
            return
        except OSError:
            return


def recv_msg(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message == "bye":
                print("Disconnected from server")
                client_socket.close()
                break
            elif message == "arret":
                print("Server stopped")
                client_socket.close()
                return
            else:
                print(message)
        except ConnectionResetError:
            print(f"Le serveur a fermé la connexion!")
            client_socket.close()
            return
        except OSError:
            return


def main(server, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server, port))
    except Exception as e:
        print(e)
        return

    print("Connected to server")
    print("Type 'bye' to quit")
    print("Type 'arret' to stop the server")

    trecv = threading.Thread(target=recv_msg, args=(s,))
    twrite = threading.Thread(target=send_msg, args=(s,))

    trecv.start()
    twrite.start()

    trecv.join()


if __name__ == '__main__':
    main("0.0.0.0", 9990)
