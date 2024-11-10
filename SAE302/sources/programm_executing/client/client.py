import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 9999))

client.send("run".encode())
print(client.recv(1024).decode())
print(client.recv(1024).decode())