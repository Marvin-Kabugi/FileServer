import socket
import threading
import os
import ssl
from search import SearchAlgorithms
from file import FileReader
import datetime

from helper_functions import measure_execution_time, load_config_file


def handle_client(client_socket: socket.socket, file_reader: FileReader) -> None:
    """
    Handle communication with a client socket.

    This function reads data from the client socket, processes the data,
    performs a search operation using the provided file reader, and sends
    back a response to the client.

    Parameters:
        client_socket (socket.socket): The socket connection to the client.
        file_reader (FileReader): An instance of the FileReader class for reading data.

    Returns:
        None

    Raises:
        socket.error: If there is an issue with the socket communication.
        ConnectionResetError: If the client connection is reset unexpectedly.
    """

    file_contents = file_reader.file_content 
    file_contents.sort()
    file_load_execution_time = measure_execution_time(1, file_reader.on_reread_selector)
    sort_exection_time = measure_execution_time(1, file_contents.sort)

 

    try:

        while True:
            data = client_socket.recv(1024)

            if not data:
                break

            if len(data) > 1024:
                response = 'DATA TOO LARGE\n'
            elif len(data) == 0:
                response = 'EMPTY DATA\n'

            search_value = data.decode().rstrip("\x00")
            requesting_ip = client_socket.getpeername()[0]
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            debug_log = f"DEBUG: Search query: '{search_value}', from IP Adress: {requesting_ip}, at: {current_time}"
            print(debug_log)

            response = None

            if file_reader.reread_on_query:
                file_contents = file_reader.on_reread_selector()
                file_contents.sort()
 
                file_load_execution_time = measure_execution_time(1, file_reader.on_reread_selector)
                sort_exection_time = measure_execution_time(1, file_contents.sort)
                total = file_load_execution_time + sort_exection_time


            result = SearchAlgorithms().binary_search(file_contents, search_value)
            search_execution_time = measure_execution_time(1, SearchAlgorithms().binary_search, file_contents, search_value)

            if file_reader.reread_on_query:
                debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}" 
            else:
                debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}" 

            print(debug_log)

            response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'          
            client_socket.send(response.encode())

    except (socket.error, ConnectionResetError) as e:
        raise e
    finally:
        client_socket.close()

# This function binds and listens for connections from the client
def main():
    """
    Start a server that binds to a port and handles multiple client connections using threading.

    This function initializes a server that listens on a specific host and port.
    It accepts incoming client connections and creates separate threads to handle
    communication with each client. The server remains active until terminated.

    Returns:
        None

    Raises:
        KeyboardInterrupt: If the server is manually interrupted by the user.
    """

    REREAD_ON_QUERY = False
    path, ssl_settings = load_config_file()
    print(path, ssl_settings)
    

    if path is None:
        return
    
    file_reader = FileReader(path, REREAD_ON_QUERY)
    HOST = "127.0.0.1"
    PORT = 65449

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()



    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f'client is {addr}')
            if ssl_settings:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                working_dir = os.path.dirname(os.path.abspath(__file__))
                # print(working_dir, "hey",__file__)
                key = os.path.join(working_dir, 'Keys', 'key.pem')
                cert = os.path.join(working_dir, 'Keys', 'cert.pem')
                # print(key, "hey", cert)

                context.load_cert_chain(certfile=cert, keyfile=key, password='pass')
                
                client_socket = context.wrap_socket(client_socket, server_side=True)

            client_thread = threading.Thread(target=handle_client, args=(client_socket, file_reader))
            client_thread.start()

    except KeyboardInterrupt as e:
        print("Socket closed")
        server_socket.close()
        raise e
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
