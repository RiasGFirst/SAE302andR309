import socket
import time
import json
import os


def file_services(client_socket, client_id):
    server_dir = os.getcwd()
    if not os.path.exists(f"{server_dir}/client/{client_id}"):
        os.makedirs(f"{server_dir}/client/{client_id}")
        print(f"Directory {client_id} created")
    try:
        client_socket.send("<CLIENT_FILE_START>".encode())
        print("First message sent")
        time.sleep(0.5)
        file_name = client_socket.recv(1024).decode()
        file_extension = file_name.split(".")[-1]

        extensions = ['cpp', 'c', 'java', 'py']
        with open(f"{server_dir}/files/compilateurs.json", "r") as file:
            data = json.load(file)
            if file_extension not in extensions:
                client_socket.send("<CLIENT_FILE_ERROR>".encode())
                print("Extension not supported")
                return
            ext_lang_mapping = {
                "cpp": "C++",
                "c": "C",
                "java": "Java",
                "py": "Python"
            }
            language = ext_lang_mapping.get(file_extension)

            # Vérifier si le langage est exécutable
            if language and data.get(language, False):
                client_socket.send("<CLIENT_FILE_OK>".encode())
                print("File accepted")
                time.sleep(0.5)
                file_size = client_socket.recv(1024).decode()
                print(file_size)
                client_socket.send("<CLIENT_FILE_SIZE_OK>".encode())
                print("File size received")
                time.sleep(0.5)

                file = open(f"{server_dir}/client/{client_id}/{file_name}", "wb")
                file_bytes = b""

                done = False
                while not done:
                    data = client_socket.recv(1024)
                    if file_bytes[-5:] == b"<END>":
                        done = True
                    else:
                        file_bytes += data

                file.write(file_bytes[:-5])
                file.close()
                client_socket.send("<CLIENT_FILE_RECEIVED>".encode())
                print("File received")
            else:
                client_socket.send("<CLIENT_FILE_ERROR>".encode())
                time.sleep(0.5)
                client_socket.send("Le langage n'est pas supporté.".encode())
                return
    except OSError:
        print("Erreur lors de la réception du fichier.")
        return
    except ConnectionResetError:
        print("Client disconnected")
        return
    except ConnectionAbortedError:
        print("Client disconnected")
        return
    except Exception as e:
        print(e)
        return

