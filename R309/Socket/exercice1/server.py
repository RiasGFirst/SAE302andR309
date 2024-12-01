import socket

def main(host, port, reply):
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    data = conn.recv(1024).decode()
    print("Data received: " + data)
    conn.send(reply.encode())
    conn.close()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 9990
    reply = "Hello client"
    main(host, port, reply)