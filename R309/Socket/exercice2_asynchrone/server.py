import socket
import threading

def handle_client(client_socket):
    





def test():
    while True:

        # Receive data from the client
        data = client.recv(1024)
        if not data:
            break
        message = data.decode()
        match message:
            case "bye":
                print("Client has closed the connection")
                client.send("bye".encode())
                nb_msg = 0
                break
            case "arret":
                print("Server has been stopped")
                client.send("bye".encode())
                arret = True
                break
            case _:
                print(f"Client says: {data.decode()}")
                nb_msg += 1
                client.send(f"You send {nb_msg} messages".encode())
    if arret:
        break




def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((socket.gethostname(), 1234))
    server.listen(5)

    print("Server started.")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    main()