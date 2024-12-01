import socket
import time


def check_server(server) -> str:
    """
    Check if the server is available
    :param server: Server object
    :return: "AVAILABLE" if server is available, "UNAVAILABLE" otherwise
    """
    address = server["IP"]
    port = server["PORT"]
    password = server["PASSWORD"]


    client_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_server.connect((address, port))
        client_server.send("<CLIENT_AUTH>".encode())
        msg = client_server.recv(1024).decode()
        if msg == "<SEND_CLIENT_ID>":
            time.sleep(0.5)
            client_server.send("server".encode())
            time.sleep(0.5)
            client_server.send(password.encode())
            response = client_server.recv(1024).decode()
            if response == "<SERVER_AUTH_SUCCESS>":
                msg = client_server.recv(1024).decode()
                if msg == "<SERVER_NOT_AVAILABLE>":
                    client_server.close()
                    return "UNAVAILABLE"
                elif msg == "<SERVER_AVAILABLE>":
                    client_server.close()
                    return "AVAILABLE"
                else:
                    print("Unknown response from server")
                    client_server.close()
                    return "UNAVAILABLE"
            elif response == "<SERVER_AUTH_FAILED>":
                print("Server authentication failed")
                client_server.close()
                return "UNAVAILABLE"
            else:
                print("Unknown response from server")
                client_server.close()
                return "UNAVAILABLE"
        else:
            print("Unknown response from server")
            client_server.close()
            return "UNAVAILABLE"

    except Exception as e:
        print("Error: %s" % e)
        client_server.close()
        return "UNAVAILABLE"