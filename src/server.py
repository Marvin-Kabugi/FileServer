import socket
import threading
import os
import ssl
import datetime
import time
from concurrent.futures import ThreadPoolExecutor


lock = threading.Lock()


def extract_element(buffer: str) -> (str, str):
    """Extract the first element (up to the eighth semicolon) from the buffer and return the element and the updated buffer."""
    semicolon_count = 0
    position = 0

    for char in buffer:
        # print('x',char)
        if char == ";":
            semicolon_count += 1
        position += 1
        if semicolon_count == 8:
            break

    if semicolon_count == 8:
        return buffer[:position], buffer[position:], True
    else:
        return None, buffer, False


def handle_client(client_socket: socket.socket, file_reader, search_algorithm, timer) -> None:
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
    with lock:
        file_contents.sort()
    file_load_execution_time = timer(1, file_reader.on_reread_selector)
    sort_exection_time = timer(1, file_contents.sort)
    buffer = ""

    try:
        while True:
            data = client_socket.recv(1024)
            # print(data)
            if len(data) == 0:
                break

            buffer = data.decode().rstrip("\x00")
            print(buffer)
            element, buffer, full_element_found = extract_element(buffer)

            # while element or buffer:
            if element:
                search_value = element
                print('this is the search value', search_value)
                requesting_ip = client_socket.getpeername()[0]
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"DEBUG: REREAD_ON_QUERY: {file_reader.reread_on_query}")
                debug_log = f"DEBUG: Search query: '{(search_value)}', from IP Adress: {requesting_ip}, at: {current_time}"
                print(debug_log)

                # response = None
                if file_reader.reread_on_query:
                    file_contents = file_reader.on_reread_selector()
                    with lock:
                        file_contents.sort()
                    # print(file_contents)

                    file_load_execution_time = timer(
                        1, file_reader.on_reread_selector)
                    # print("file_load_execution_time:", file_load_execution_time)
                    sort_exection_time = timer(1, file_contents.sort)
                    # print("sort_exection_time:",sort_exection_time)
                    total = file_load_execution_time + sort_exection_time

                result = search_algorithm.binary_search(
                    file_contents, search_value)
                print('this is the result:', result)
                search_execution_time = timer(
                    1, search_algorithm.binary_search, file_contents, search_value)

                if file_reader.reread_on_query:
                    debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}\n"
                else:
                    debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}\n"

                print(debug_log)

                response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'
                client_socket.sendall(response.encode())

            if buffer:
                # response = 'STRING NOT FOUND\n'
                # buffer = ""
                search_value = buffer
                print('this is the search value', search_value)
                requesting_ip = client_socket.getpeername()[0]
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"DEBUG: REREAD_ON_QUERY: {file_reader.reread_on_query}")
                debug_log = f"DEBUG: Search query: '{(search_value)}', from IP Adress: {requesting_ip}, at: {current_time}"
                print(debug_log)

                # response = None
                if file_reader.reread_on_query:
                    file_contents = file_reader.on_reread_selector()
                    with lock:
                        file_contents.sort()
                    # print(file_contents)

                    file_load_execution_time = timer(
                        1, file_reader.on_reread_selector)
                    # print("file_load_execution_time:", file_load_execution_time)
                    sort_exection_time = timer(1, file_contents.sort)
                    # print("sort_exection_time:",sort_exection_time)
                    total = file_load_execution_time + sort_exection_time

                result = search_algorithm.binary_search(
                    file_contents, search_value)
                print('this is the result:', result)
                search_execution_time = timer(
                    1, search_algorithm.binary_search, file_contents, search_value)

                if file_reader.reread_on_query:
                    debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}\n"
                else:
                    debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}\n"

                print(debug_log)

                response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'

                client_socket.sendall(response.encode())

            # element, buffer, full_element_found = extract_element(buffer)

            # if not full_element_found:
            #     break
    except (socket.error, ConnectionResetError) as e:
        raise e
    # client_socket.close()

    finally:
        client_socket.close()

# This function binds and listens for connections from the client


def main(path, ssl_settings, search_algorithm, file_reader, timer, socket_settings):
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

    ssl_toggle = True if ssl_settings == "True" else False

    if path is None:
        return

    HOST, PORT = socket_settings
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Failed to create socket.")

    try:
        server_socket.bind((HOST, PORT))
    except socket.gaierror as e:
        print(f'Address-related error connecting to server:{e}')

    server_socket.listen()
    print("listening")

    futures = []
    try:
        while True:

            client_socket, addr = server_socket.accept()

            if ssl_toggle:
                print(ssl_settings)
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                working_dir = os.path.dirname(os.path.abspath(__file__))
                print(working_dir, "hey", __file__)
                key = os.path.join(working_dir, 'Keys', 'key.pem')
                cert = os.path.join(working_dir, 'Keys', 'cert.pem')
                # print(key, "hey", cert)

                context.load_cert_chain(
                    certfile=cert, keyfile=key, password='pass')

                client_socket = context.wrap_socket(
                    client_socket, server_side=True)

            # Or however many threads you want to allow.
            executor = ThreadPoolExecutor(max_workers=10)
            future = executor.submit(
                handle_client, client_socket, file_reader, search_algorithm, timer)
            futures.append(future)

    except KeyboardInterrupt as e:
        print("Waiting for active threads to finish...")
        for future in futures:
            # This will block until the future (thread) has completed.
            future.result()
        print("Socket closed")
        server_socket.close()
        raise e
    finally:
        server_socket.close()
