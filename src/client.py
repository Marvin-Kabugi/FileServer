import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024).decode()

# print(f"Received {data!r}")

try:
    # create socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    client_socket.connect((HOST, PORT))
    print("Connected to the server")

    # create and send message to the server
    message="22;0;6;28;0;23;3;0;"
    client_socket.send(message.encode())

    # receive data from the server
    data = client_socket.recv(1024)
    print(data.decode())
except socket.error as e:
    raise e

finally:
    client_socket.close()
    print("Socket Closed")


