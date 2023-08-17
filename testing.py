import socket

# Server information
server_ip = "135.181.96.160"  # Replace with the actual IP address
server_port = 44445      # Replace with the actual port number
ssl_enabled = False     # SSL is set to False
REREAD_ON_QUERY = "REREAD_ON_QUERY"

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect((server_ip, server_port))
    print("Connected to the server")

    # Send data to the server (optional)
    message = f"8;0;23;28;0;24;3;0;\x00"
    client_socket.send(message.encode())

    # Receive data from the server (optional)
    data = client_socket.recv(1024)
    print("Received from server:", data.decode())

except socket.error as e:
    print("Error:", e)

finally:
    # Close the socket
    client_socket.close()
    print("Socket closed")
