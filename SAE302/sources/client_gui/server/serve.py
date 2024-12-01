import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345))
server.listen(1)
print("Serveur en attente de connexions...")
conn, addr = server.accept()
print(f"Connexion de {addr}")
while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Reçu : {data.decode('utf-8')}")
    conn.sendall(f"Message reçu : {data.decode('utf-8')}".encode('utf-8'))
