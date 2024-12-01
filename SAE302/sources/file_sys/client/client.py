import socket
import time
import uuid
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 9999))
client_uuid = str(uuid.uuid4())[0:8]

file_path = str(input("Enter the file path: "))
file_name = file_path.split('/')[-1]

file = open(file_path, 'rb')
file_size = os.path.getsize(file_path)


client.send(client_uuid.encode())
time.sleep(1)
client.send(file_name.encode())
time.sleep(1)
client.send(str(file_size).encode())

data = file.read()
client.sendall(data)
client.send(b"<END>")

file.close()
client.close()
