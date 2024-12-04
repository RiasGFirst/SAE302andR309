import socket
import time
import json
import os


def file_services(client_socket, client_id):
    server_dir = os.getcwd()
    if not os.path.exists(server_dir + '/client/' + client_id):
        os.makedirs(server_dir + '/client/' + client_id)
    client_dir = server_dir + '/client/' + client_id
    client_socket.send('<FILE_SERVICE>'.encode())
    time.sleep(0.1)
    client_socket.send('<FILE_DATA_REQUESTS>'.encode())
    file_name = client_socket.recv(1024).decode()
    file_size = client_socket.recv(1024).decode()
    print(file_name, file_size)
    if check_extension(file_name, server_dir):
        client_socket.send('<FILE_DATA_READY>'.encode())

        file = open(f"{client_dir}/{file_name}", "wb")
        file_bytes = b""
        done = False

        while not done:
            data = client_socket.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b'<END>':
                print("File done")
                done = True
            else:
                print("File bytes received: ", file_bytes)

        print(file_bytes[:-5])
        print("File bytes received")
        print(file)
        file.write(file_bytes[:-5])
        print("File received")
        file.close()
        print("File closed")
        client_socket.send('<FILE_RECEIVED>'.encode())
    else:
        client_socket.send('<FILE_DATA_NOT_READY>'.encode())
        return





def check_extension(file_name, server_dir):
    # {"C": true, "C++": true, "Java": false, "Python": true}
    extension_allowed = ["py", "c", "cpp", "cc", "java"]
    file_extension = file_name.split('.')[-1]
    print(f"File extension: {file_extension}")

    if file_extension not in extension_allowed:
        return False
    else:
        if os.path.exists(f'{server_dir}/files/compilateurs.json'):
            print("File exists")
            with open(f'{server_dir}/files/compilateurs.json') as f:
                data = json.load(f)
                for key in data:
                    dir_extension = {
                        "py": "Python",
                        "c": "C",
                        "cpp": "C++",
                        "cc": "C++",
                        "java": "Java"
                    }
                    if key == dir_extension[file_extension]:
                        return data[key]
