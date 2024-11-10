import socket

def main():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get local machine name
    host = str(input("Enter the hostname: "))

    port = int(input("Enter the port number: "))

    # Connection to hostname on the port.
    s.connect((host, port))
    # Receive no more than 1024 bytes
    msg = s.recv(1024)
    print(msg.decode('utf-8'))
    s.send("Hello, Server!".encode("utf-8"))
    msg = s.recv(1024)
    print(msg.decode('utf-8'))
    s.close()


if __name__ == '__main__':
    main()