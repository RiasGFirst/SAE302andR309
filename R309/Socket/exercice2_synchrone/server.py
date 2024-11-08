import socket


def main(host, port):
    #Create a socket object to instantiate the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Bind the server to a specific port
    server.bind((host, port))

    #Listen for incoming connections
    server.listen(1)

    print(f"Server is listening on {host}:{port}")
    connection(server)


def connection(server):
    nb_msg = 0
    arret = False
    # Accept incoming connections
    while True:
        client, address = server.accept()
        print(f"Connection from {address} has been established!")

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

        
if __name__ == "__main__":
    host = socket.gethostname()
    port = 6969
    main(host, port)