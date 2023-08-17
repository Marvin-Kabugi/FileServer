import socket
import threading
import os
import re
from typing import List
from search import SearchAlgorithms
from file import FileReader



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
    script_directory = os.path.dirname(os.path.abspath(__file__))
    config = os.path.join(script_directory, 'config.txt')
    # config = os.path.join('src', 'config.txt')
    required_path = None
    # print(config)
    if os.path.exists(config):
        try:
            with open(config, 'r') as con:
                for line in con:
                    if line.startswith("linuxpath="):
                        required_path = line.strip().split('=')[1]
                        break
        except FileNotFoundError:
            print("File not found")
    if required_path is None:
        print("No path found in the config file")
    else:
        data_path = required_path
        return data_path


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
            file_contents = file_reader.on_reread_selector()
            response = SearchAlgorithms().linear_search(file_contents, search_value)

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
    REREAD_ON_QUERY = False
    path = load_config_file()
    print(path)

    if path is None:
        return

    file_reader = FileReader(path, REREAD_ON_QUERY)

    HOST = "127.0.0.1"
    PORT = 65432  

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f'client is {addr}')
            client_thread = threading.Thread(target=handle_client, args=(client_socket, file_reader))
            client_thread.start()
    except KeyboardInterrupt as e:
        print("Socket closed")
        raise e
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()











# def load_files(path: str) -> str:
#     try:
#         with open(path, "r") as file:
#             print("opening")
#             lines = file.readlines()
#             lines = [line.strip() for line in lines]
#             filtered_lines = filter_duplicates(lines)
#             for line in filtered_lines:
#                 yield line
#     except FileNotFoundError:
#         print("File not found")


# def grep_search(path, search_value):
#     command = f"grep ^{search_value}$ {path}"
#     os.system(command)

# def linear_search(path,search_value):
#     try:
#         with open(path, 'r') as file:
#             print("opening")
#             for line in file:
#                 if line.strip() == search_value:
#                     return ("STRING EXISTS")
#             return ("STRING NOT FOUND")
#     except FileNotFoundError as e:
#         return ("File does not Exist")
    
# def search_using_regex(path, searchvalue):
#     try:
#         with open(path, 'r') as file:
#             print("opening")
#             for line in file:
#                 if re.fullmatch(f'^{searchvalue}$', line.strip()):
#                     return ("STRING EXISTS")
#             return ("STRING NOT FOUND")
#     except FileNotFoundError as e:
#         return ("File does not Exist")import socket


# def load_files(path: str) -> str:
#     try:
#         with open(path, "r") as file:
#             print("opening")
#             lines = file.readlines()
#             lines = [line.strip() for line in lines]
#             filtered_lines = filter_duplicates(lines)
#             for line in filtered_lines:
#                 yield line
#     except FileNotFoundError:
#         print("File not found")


# def grep_search(path, search_value):
#     command = f"grep ^{search_value}$ {path}"
#     os.system(command)

# def linear_search(path,search_value):
#     try:
#         with open(path, 'r') as file:
#             print("opening")
#             for line in file:
#                 if line.strip() == search_value:
#                     return ("STRING EXISTS")
#             return ("STRING NOT FOUND")
#     except FileNotFoundError as e:
#         return ("File does not Exist")
    
# def search_using_regex(path, searchvalue):
#     try:
#         with open(path, 'r') as file:
#             print("opening")
#             for line in file:
#                 if re.fullmatch(f'^{searchvalue}$', line.strip()):
#                     return ("STRING EXISTS")
#             return ("STRING NOT FOUND")
#     except FileNotFoundError as e:
#         return ("File does not Exist")