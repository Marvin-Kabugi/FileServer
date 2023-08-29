import socket
import time

from src.file import FileReader
from src.client import Client


# Server information
server_ip = "135.181.96.160"  # Replace with the actual IP address
server_port = 44445      # Replace with the actual port number
ssl_enabled = False     # SSL is set to False
REREAD_ON_QUERY = "REREAD_ON_QUERY"

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     # Connect to the server
#     client_socket.connect((server_ip, server_port))
#     print("Connected to the server")

    # Send data to the server (optional)
    # message = "Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)Receive data from the server (optional)"
message = ['3;0;1;28;0;7;5;0;', '10;0;1;26;0;8;3;0;', '18;0;6;28;0;23;5;0;', '7;0;1;28;0;9;3;0;', '22;0;6;28;0;23;3;0;', '7;0;6;28;0;23;5;0;', '2;0;1;26;0;7;5;0;', '10;0;1;26;0;7;4;0;', '7;0;1;26;0;8;3;0;', '13;0;1;28;0;7;4;0;']
file = FileReader("/home/jmarvin/Development/Projects/AlgorithmicSciences/Files/10000.txt",True)
    # for s_message in file.file_content[10:20]:
    #             # print(s_message)y
    #     time.sleep(0.2)
    #     client_socket.send(s_message.encode())
    # client_socket.send(message.encode())
#     client_socket.sendall(b'')
#     data_x = ''
#     while True:
#     # Receive data from the server (optional)
#         data = client_socket.recv(1024)
#         if len(data) <= 0:
#             break
#         data_x += data.decode()
#         print(data.decode())
#     # print("Received from server:", data_x)
#     # print("j")
# except socket.error as e:
#     print("Error:", e)

# finally:
#     # Close the socket
#     client_socket.close()
#     print("Socket closed")

client = Client(server_ip, server_port)
(client.send_message(file.file_content))