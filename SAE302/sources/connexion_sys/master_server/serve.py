from utils.check_compilor import verify_compile
from models.Server import Server
import sys
import os


def help():
    print("""
    SERTUP THE SERVER:
    Usage: python serve.py install
    This will check if you have the compilers installed on your machine
    
    RUN THE SERVER:
    Usage: python serve.py run <server_type> <port> <clientmax>
    server_type: master, slave
    port: the port number to run the server on
    clientmax: the maximum number of clients the server can accept
    Example: python serve.py master 5000 2
    """)


def serve():
    args = sys.argv
    if len(args) < 2:
        help()
        return
    match args[1]:
        case "install":
            compilateurs = {
                "C": "gcc",
                "C++": "g++",
                "Java": "javac",
            }
            verify_compile(compilateurs)
        case "run":
            if len(args) < 5:
                help()
                return
            server_type = args[2]
            port = int(args[3])
            clientmax = int(args[4])
            if server_type not in ["master", "slave"]:
                print("Invalid server type")
                help()
                return
            if not os.path.exists(f"{os.getcwd()}/files/compilateurs.json"):
                print("Please run the command 'python serve.py install' to check the compilers")
                return
            server = Server(name=server_type, port=port, clientmax=clientmax)
            server.run_serve()
        case _:
            help()


if __name__ == '__main__':
    serve()
