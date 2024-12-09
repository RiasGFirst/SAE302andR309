import utils.compile_services as compile_services
import time
import json
import os


def file_services(client_socket, client_id):
    server_dir = os.getcwd()
    if not os.path.exists(server_dir + '/client/' + client_id):
        os.makedirs(server_dir + '/client/' + client_id)
    client_dir = server_dir + '/client/' + client_id
    client_socket.send('<FILE_SERVICE>'.encode())
    print(f"[*] Client {client_id} has initialised the compilation process")
    time.sleep(0.1)
    client_socket.send('<FILE_DATA_REQUESTS>'.encode())
    file_name = client_socket.recv(1024).decode()
    file_size = client_socket.recv(1024).decode()
    print(f"[*] Client {client_id} has sent the file {file_name} of size {file_size} bytes")
    if check_extension(file_name, server_dir):
        client_socket.send('<FILE_DATA_READY>'.encode())

        file = open(f"{client_dir}/{file_name}", "wb")
        file_bytes = b""
        done = False

        while not done:
            data = client_socket.recv(1024)
            file_bytes += data
            if file_bytes[-5:] == b'<END>':
                done = True

        file.write(file_bytes[:-5])
        file.close()
        client_socket.send('<FILE_RECEIVED>'.encode())
        print(f"[*] The file {file_name} has been received successfully")

        compile_services.compile(client_socket, f"{client_dir}/{file_name}", client_id)
    else:
        client_socket.send('<FILE_DATA_NOT_READY>'.encode())
        return


def check_extension(file_name, server_dir):
    # {"C": true, "C++": true, "Java": false, "Python": true}
    extension_allowed = ["py", "c", "cpp", "cc", "java"]
    file_extension = file_name.split('.')[-1]

    if file_extension not in extension_allowed:
        return False
    else:
        if os.path.exists(f'{server_dir}/files/compilateurs.json'):
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
