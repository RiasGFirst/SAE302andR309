import argparse
import socket
import time

def client(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send("<CLIENT_AUTH>".encode())
    if s.recv(1024).decode() == "<SEND_CLIENT_ID>":
        s.send("client".encode())
        time.sleep(1)
        username = input("Enter username: ")
        password = input("Enter password: ")
        s.send(username.encode())
        time.sleep(0.5)
        s.send(password.encode())
        msg = s.recv(1024).decode()
        if msg == "<CLIENT_AUTH_SUCCESS>":
            print(f"Client authenticated with id: {username}")

            auth_send = s.recv(1024).decode()

            if auth_send == "<SEND_CLIENT_DATA>":
                s.send(f"I'm {username}".encode())
                time.sleep(1)
                s.send("Hello World!".encode())
                time.sleep(60)
                s.send("<CLIENT_QUIT>".encode())
                s.close()
            elif auth_send == "<CLIENT_EXCEEDED>":
                msg = s.recv(1024).decode()
                time.sleep(0.5)
                if msg == "<SERVER_AVAILABLE>":
                    data = s.recv(1024).decode()
                    print(f"Please login on {data}")
                    s.close()
                else:
                    print("No server available")
                    s.close()
            else:
                print("We don't want to connect to the server :)")
                s.close()
        elif msg == "<CLIENT_ALREADY_CONNECTED>":
            print("Client already connected")
            s.close()
        elif msg == "<CLIENT_AUTH_FAILED>":
            print("Authentication failed")
            s.close()
        else:
            print("We don't want to connect to the server :)")
            s.close()
    else:
        print("Authentication failed")
        s.close()

if __name__ == "__main__":
    # Creer des arguments pour le port
    parser = argparse.ArgumentParser(description="Servers")
    parser.add_argument("-p", "--port", type=int, help="Port d'écoute du serveur", default=9999)
    args = parser.parse_args()
    client("127.0.0.1", args.port)