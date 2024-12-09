import subprocess
import os
import time


def compile(client_socket, file_name, client_id):
    client_socket.send(f"<EXEC_FILE>".encode())
    msg = client_socket.recv(1024).decode()

    if msg == "<EXEC_FILE_READY>":
        print(f"[*] File from {client_id} is ready to be compiled")
        file_extension = file_name.split('.')[-1]

        if file_extension == "py":
            client_socket.send("<PYTHON>".encode())
            msg1 = compile_python(file_name)
            client_socket.send(msg1.encode())
        elif file_extension == "c":
            client_socket.send("<C>".encode())
            m1, m2 = compile_c(file_name, client_id)
            if m1 is not None:
                client_socket.send(m1.encode())
            else:
                client_socket.send(m2.encode())
        elif file_extension == "cpp" or file_extension == "cc":
            client_socket.send("<CPP>".encode())
            m1, m2 = compile_cpp(file_name, client_id)
            if m1 is not None:
                client_socket.send(m1.encode())
            else:
                client_socket.send(m2.encode())
        elif file_extension == "java":
            client_socket.send("<JAVA>".encode())
            msg1 = compile_java(file_name)
            client_socket.send(msg1.encode())
        else:
            client_socket.send(f"<ERROR>".encode())
            return


def compile_python(file):
    compile_process = subprocess.run(['python', file], capture_output=True, text=True)

    if compile_process.returncode == 0:
        return compile_process.stdout
    else:
        return compile_process.stderr


def compile_c(file, client_id):
    compile_process = subprocess.run(['gcc', file, "-o", f"{os.getcwd()}/client/{client_id}/programme"], capture_output=True, text=True)

    if compile_process.returncode == 0:
        run_process = subprocess.run([f"{os.getcwd()}/client/{client_id}/programme"], capture_output=True, text=True)
        m2 = run_process.stdout
        return None, m2
    else:
        m1 = compile_process.stderr
        return m1, None


def compile_cpp(file, client_id):
    compile_process = subprocess.run(['g++', file, "-o", f"{os.getcwd()}/client/{client_id}/programme"], capture_output=True, text=True)

    if compile_process.returncode == 0:
        run_process = subprocess.run([f"{os.getcwd()}/client/{client_id}/programme"], capture_output=True, text=True)
        m2 = run_process.stdout
        return None, m2
    else:
        m1 = compile_process.stderr
        return m1, None


def compile_java(file):
    run_process = subprocess.run(['java', file], capture_output=True, text=True)

    if run_process.returncode == 0:
        return run_process.stdout
    else:
        return run_process.stderr