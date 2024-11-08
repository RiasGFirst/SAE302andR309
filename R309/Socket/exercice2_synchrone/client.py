import socket

def main():
    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = input("Enter the hostname: ")
    port = int(input("Enter the port number: "))

    # Connect to hostname on the port.
    client.connect((host, port))

    send(client)


def send(c):
    while True:
        message = input("Enter message: ")
        c.send(message.encode())
        data = c.recv(1024)
        if not data:
            break
        if data.decode() == 'bye':
            c.close()
            break
        print('Received from server: ', data.decode())


if __name__ == '__main__':
    main()