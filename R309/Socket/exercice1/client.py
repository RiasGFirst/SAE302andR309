import socket

def main(host, port, message):
    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print('Received from server: ' + data)
    client_socket.close()


if __name__ == '__main__':
    host = socket.gethostname()
    port = 6969
    message = 'Hello, server!'
    main(host, port, message)