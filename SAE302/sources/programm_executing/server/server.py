import subprocess
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 9999))

server.listen()
client, addr = server.accept()
print(f"Connection from {addr} has been established!")

action = client.recv(1024).decode()

if action == "run":
    # Compiler le programme C
    compile_process = subprocess.run(["g++", "programmc.cpp", "-o", "programme"], capture_output=True, text=True)

    # Vérifier si la compilation a réussi
    if compile_process.returncode == 0:
        client.send("Compilation réussie.".encode())
    else:
        client.send(f"Erreur de compilation : {compile_process.stderr}".encode())

    # Exécuter le programme et capturer la sortie
    run_process = subprocess.run(["./programme"], capture_output=True, text=True)

    # Envoyer la sortie au client
    client.send(run_process.stdout.encode())

    client.close()
    server.close()
