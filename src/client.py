import socket
import ssl
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65449
SSL = True  # The port used by the server


try:
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if SSL:
        context = ssl.create_default_context()
        working_dir = os.path.dirname(os.path.abspath(__file__))
        server_cert = os.path.join(working_dir, 'cert.pem')
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # print(server_cert)
        # context.load_verify_locations(cafile=server_cert)
        client_socket = context.wrap_socket(client_socket, server_hostname=HOST)

    # connect to the server
    client_socket.connect((HOST, PORT))
    print("Connected to the server")

    # create and send message to the server
    message="13;0;23;11;0;16;5;0;"
    client_socket.send(message.encode())

    # receive data from the server
    data = client_socket.recv(1024)
    print(data.decode())
except socket.error as e:
    raise e

finally:
    client_socket.close()
    print("Socket Closed")


