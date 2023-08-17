import socket
import threading
import concurrent.futures


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def thread_func(client_socket):
    try:
        while client_socket:
            data = client_socket.recv(1024).decode()

            if not data:
                return

            response = "STRING EXISTS"
            client_socket.send(response.encode())
    except Exception as e:
        print("Error:", e)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            new_socket, addr = server_socket.accept()
            executor.submit(thread_func, new_socket)
            

            



