import socket
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 9999))

server.listen()

client, addr = server.accept()

# Creation of the client directory
client_uuid = client.recv(1024).decode("utf-8")
print(f"Received request for {client_uuid}")

server_dir = os.getcwd()
if not os.path.exists(f"{server_dir}/client/{client_uuid}"):
    os.makedirs(f"{server_dir}/client/{client_uuid}")
    print(f"Directory {client_uuid} created")

# File Sending System
file_name = client.recv(1024).decode("utf-8")
print(f"Received request for {file_name}")

file_size = client.recv(1024).decode("utf-8")
print(f"File size: {file_size}")

file = open(f"{server_dir}/client/{client_uuid}/{file_name}", "wb")
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