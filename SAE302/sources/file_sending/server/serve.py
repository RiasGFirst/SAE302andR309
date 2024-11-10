import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 9999))

server.listen()

client, addr = server.accept()

file_name = client.recv(1024).decode("utf-8")
print(f"Received request for {file_name}")

file_size = client.recv(1024).decode("utf-8")
print(f"File size: {file_size}")

file = open(file_name, "wb")

file_bytes = b""

done = False

while not done:
    data = client.recv(1024)
    if file_bytes[-5:] == b"<END>":
        done = True
    else:
        file_bytes += data

file.write(file_bytes[:-5])

file.close()
print("File received")

client.close()
server.close()