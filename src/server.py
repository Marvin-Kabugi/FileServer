import socket
import threading
import os
import ssl
from search import SearchAlgorithms
from file import FileReader
import time
import timeit





def load_config_file() -> str:
    """
    Load the path from the configuration file.

    This function reads the 'config.txt' file located in the same directory as
    the script and searches for a line starting with 'linuxpath='. If found,
    it extracts the path following the prefix and returns it.

    Returns:
        str: The path extracted from the configuration file.

    Note:
        If the 'config.txt' file is not found or no valid path is found in the
        file, this function will print appropriate messages and return None.

    Example:
        If the 'config.txt' file contains a line:
        linuxpath=/root/mydata.txt

        Calling load_config_file() would return '/root/200k.txt'.
    """
    # script_directory = os.path.dirname(os.path.abspath(__file__))
    script_directory = os.path.abspath(os.getcwd())
    config = os.path.join(script_directory, 'config.txt')
    required_path = None
    ssl_settings = None
    if os.path.exists(config):
        try:
            with open(config, 'r') as con:
                for line in con:
                    if line.startswith("linuxpath="):
                        required_path = line.strip().split('=')[1]
                    if line.startswith("SSL="):
                        ssl_settings = line.strip().split("=")[1]
        except FileNotFoundError:
            print("File not found")
    if required_path is None:
        print("No path found in the config file")
    else:
        data_path = required_path
        return (data_path, ssl_settings)


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
    try:

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            search_value = data.decode().rstrip("\x00")
            file_contents = None
            response = None
            if file_reader.reread_on_query:
                st = time.time()
                file_contents = file_reader.on_reread_selector()
                et = time.time()
                elapsed_time = (et - st) * 1000  # Convert to milliseconds
                print(elapsed_time, "2")
                # print(search_value in file_contents)
                # st_search = time.time()
                result = SearchAlgorithms().binary_search(file_contents, search_value)
                response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'
                # et_search = time.time()
                # elapsed_search_time = (et_search - st_search) * 1000  # Convert to milliseconds
                # print(elapsed_search_time)
                
            
            else:
                st = time.time()
                file_contents = file_reader.file_content
                et = time.time()
                elapsed_time = (et - st) * 1000  # Convert to milliseconds
                print(elapsed_time, "2")                
                result = SearchAlgorithms().binary_search(file_contents, search_value)
                response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'

            if file_reader.reread_on_query:
                print("Measuring actual execution time...")
                number = 1000
                actual_execution_time = timeit.timeit(
                    lambda: SearchAlgorithms().binary_search(file_contents, search_value),
                    number=number  # You can adjust the number of repetitions for better accuracy
                )
                print(f"Actual execution time (ms): {(actual_execution_time * 1000)/number:.4f}")
            client_socket.send(response.encode())

    except (socket.error, ConnectionResetError) as e:
        print(e)
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

    REREAD_ON_QUERY = True
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
                print(key, "hey", cert)

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
    # n = 5
    # result = timeit.timeit(stmt='main()', globals=globals(), number=n)
    # print("hey")
    # print(f'Execution time is {result}')
    main()
