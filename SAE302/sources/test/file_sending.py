import os


def file_sending(client_socket, client_name):
    directory = os.getcwd()
    client_directory = f"{directory}/client/{client_name}"
    file_name = client_socket.recv(1024).decode()
    # Verify the extension of the file
    isFileOK = verify_extension(file_name)
    if not isFileOK:
        print(f"File {file_name} is not allowed to be sent from {client_name}.")
        client_socket.send("<FILE_ERROR>###File Not Allowed !".encode())
        return
    file_size = int(client_socket.recv(1024).decode())
    print(f"Receiving file {file_name} ({file_size}B) from {client_name}...")
    client_socket.send("<FILE_SENDING>###File Allowed, Starting transfering !".encode())

    file_bytes = b""
    done = False

    while not done:
        data = client_socket.recv(1024)
        if file_bytes[-5:] == b"<FILE_SENT>":
            done = True
        else:
            file_bytes += data

    with open(f"{client_directory}/{file_name}", "wb") as file:
        file.write(file_bytes[:-len("<FILE_SENT>")])

    print(f"File {file_name} received from {client_name}.")
    client_socket.send("<FILE_RECEIVED>###File received successfully !".encode())


def verify_extension(file_name):
    extension = file_name.split(".")[-1]
    list_extension = [".cpp", ".cc", ".c", ".java", ".py"]
    if extension not in list_extension:
        return False
    return True