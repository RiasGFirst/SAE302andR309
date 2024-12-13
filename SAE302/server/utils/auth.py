# Description: Ce fichier contient les fonctions d'authentification des clients et des serveurs

from utils.check_server import check_server
import json
import time
import os


def authentificate(client_socket, client_connected, max_client=1) -> (str, dict):
    ctype, cid = login(client_socket, client_connected)
    if ctype is None and cid is None:
        print(f"\033[31m[*] Client has been rejected!\033[0m")
        return None, None
    client_type = ctype
    client_id = cid
    print(f"\033[32m[*] {client_type} {client_id} has passed authentication!\033[0m")

    # verify if a client is already connected
    print(f"client_connected: {client_connected}, len: {len(client_connected)}")
    if len(client_connected) > max_client:
        for c in client_connected:
            if c == client_id:
                print("Client is exceeding the limit")
                client_socket.send("<CLIENT_EXCEEDED>".encode())
                time.sleep(0.5)
                if os.path.exists(f"{os.getcwd()}/files/servers.json"):
                    with open(f"{os.getcwd()}/files/servers.json", "r") as file:
                        data = json.loads(file.read())
                        servers = data["SERVERS"]
                        for server in servers:
                            ok = check_server(servers[server])
                            if ok == "AVAILABLE":
                                client_socket.send("<SERVER_AVAILABLE>".encode())
                                time.sleep(0.5)
                                client_socket.send(f"{servers[server]['IP']}:{servers[server]['PORT']}".encode())
                                client_connected.remove(c)
                                print(f"\033[31m[*] {client_type} {client_id} has been ask to connect to another server!\033[0m")
                            else:
                                client_socket.send("<SERVER_NOT_AVAILABLE>".encode())
                                client_connected.remove(c)
                                print(f"\033[31m[*] {client_type} {client_id} has been rejected!\033[0m")
                return None, None
    else:
        client_socket.send("<SEND_CLIENT_DATA>".encode())
        return client_type, client_id


def login(client_socket, client_connected) -> (str, dict):
    """
    Cette fonction permet d'authentifier un client ou un serveur
    :param client_socket: socket du client
    :param client_connected: dictionnaire contenant les clients connectés
    :return: str : type de client, str : id du client
    """
    try:
        client_socket.send("<SEND_CLIENT_ID>".encode())
        client_type = client_socket.recv(1024).decode()
        if client_type == "client":
            print("We are in waiting client credentials")
            client_username = client_socket.recv(1024).decode()
            time.sleep(0.1)
            client_password = client_socket.recv(1024).decode()
            # check if the user already connected
            if client_username in client_connected:
                client_socket.send("<CLIENT_ALREADY_CONNECTED>".encode())
                return None, None
            if os.path.exists(f"{os.getcwd()}/files/users.txt"):
                with open(f"{os.getcwd()}/files/users.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        user = line.split(":")
                        if user[0] == client_username and user[1].replace("\n", "") == client_password:
                            client_socket.send("<CLIENT_AUTH_SUCCESS>".encode())
                            client_connected.append(client_username)
                            return "client", client_username
                client_socket.send("<CLIENT_AUTH_FAILED>".encode())
                return None, None
        elif client_type == "server":
            print("A server is trying to connect")
            server_password = client_socket.recv(1024).decode()
            if os.path.exists(f"{os.getcwd()}/files/servers.json"):
                with open(f"{os.getcwd()}/files/servers.json", "r") as file:
                    server = json.loads(file.read())
                    if server_password == server["PASSWORD"]:
                        client_socket.send("<SERVER_AUTH_SUCCESS>".encode())
                        time.sleep(0.5)
                        print(len(client_connected))
                        if len(client_connected) >= 1:
                            client_socket.send("<SERVER_NOT_AVAILABLE>".encode())
                            return None, None
                        else:
                            client_socket.send("<SERVER_AVAILABLE>".encode())
                            return None, None
                    else:
                        client_socket.send("<SERVER_AUTH_FAILED>".encode())
                        return None, None


    except ConnectionResetError:
        print("Client disconnected")
        return None, None
    except ConnectionAbortedError:
        print("Client disconnected")
        return None, None
    except Exception as e:
        print(e)
        return None, None