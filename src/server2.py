import socket
import threading
import os
import ssl
import datetime
import time
from concurrent.futures import ThreadPoolExecutor



lock = threading.Lock()
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

    try:
        while True:
            data = client_socket.recv(1024)
            if len(data) == 0:
                break

            print("starting")
            # print("data", data.decode())
            data_x = data.decode()
            # print(data_x)
            # response = 'STRING NOT FOUND\n'  # Default response
            responses = []  # A list to hold all responses
            found_segment = False
            count = 0
            prev = 0
            print(len(data_x))
            for i in range(len(data_x)):
                # print('hello', data_x[i])
                # print('index',i)
                # print('current', count)
                # print(data_x[i])

                if data_x[i] == ";" or i == len(data_x) - 1:
                    count += 1

                if count == 8 or i == len(data_x - 1):
                    search_value = data_x[prev: (i + 1)]
                    # print('yes', search_value)
                    # print('no', search_value.strip())
                    prev = i + 1
                    # print(prev)
                    count = 0
                    # search_value = data.decode().rstrip("\x00")
                    requesting_ip = client_socket.getpeername()[0]
                    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"DEBUG: REREAD_ON_QUERY: {file_reader.reread_on_query}")
                    debug_log = f"DEBUG: Search query: '{(search_value)}', from IP Adress: {requesting_ip}, at: {current_time}"
                    print(debug_log)

                    response = None
                    if file_reader.reread_on_query:
                        file_contents = file_reader.on_reread_selector()
                        with lock:
                            file_contents.sort()
                        # print(file_contents)
        
                        file_load_execution_time = timer(1, file_reader.on_reread_selector)
                        # print("file_load_execution_time:", file_load_execution_time)
                        sort_exection_time = timer(1, file_contents.sort)
                        # print("sort_exection_time:",sort_exection_time)
                        total = file_load_execution_time + sort_exection_time


                    result = search_algorithm.binary_search(file_contents, search_value)
                    search_execution_time = timer(1, search_algorithm.binary_search, file_contents, search_value)

                    if file_reader.reread_on_query:
                        debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}\n" 
                    else:
                        debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}\n" 

                    print(debug_log)
                    responses.append('STRING EXISTS\n' if result else 'STRING NOT FOUND\n')

                    # if result:
                    #     print(result)
                    #     response = 'STRING EXISTS\n'  
                    #     break   
                    # client_socket.sendall(response.encode())
            if not found_segment:
                final_response = 'STRING NOT FOUND\n'

            # Concatenate the responses and send to client
            final_response = ''.join(responses)
            client_socket.sendall(final_response.encode())
            # client_socket.sendall(response.encode())

            # search_value = data.decode().rstrip("\x00")
            # requesting_ip = client_socket.getpeername()[0]
            # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(f"DEBUG: REREAD_ON_QUERY: {file_reader.reread_on_query}")
            # debug_log = f"DEBUG: Search query: '{(search_value)}', from IP Adress: {requesting_ip}, at: {current_time}"
            # print(debug_log)

            # response = None
            # if file_reader.reread_on_query:
            #     file_contents = file_reader.on_reread_selector()
            #     with lock:
            #         file_contents.sort()
            #     # print(file_contents)
 
            #     file_load_execution_time = timer(1, file_reader.on_reread_selector)
            #     # print("file_load_execution_time:", file_load_execution_time)
            #     sort_exection_time = timer(1, file_contents.sort)
            #     # print("sort_exection_time:",sort_exection_time)
            #     total = file_load_execution_time + sort_exection_time


            # result = search_algorithm.binary_search(file_contents, search_value)
            # search_execution_time = timer(1, search_algorithm.binary_search, file_contents, search_value)

            # if file_reader.reread_on_query:
            #     debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}\n" 
            # else:
            #     debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}\n" 

            # print(debug_log)

            # response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'     
            # client_socket.sendall(response.encode())
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
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
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
                print(working_dir, "hey",__file__)
                key = os.path.join(working_dir, 'Keys', 'key.pem')
                cert = os.path.join(working_dir, 'Keys', 'cert.pem')
                # print(key, "hey", cert)

                context.load_cert_chain(certfile=cert, keyfile=key, password='pass')
                
                client_socket = context.wrap_socket(client_socket, server_side=True)


            executor = ThreadPoolExecutor(max_workers=10)  # Or however many threads you want to allow.
            future = executor.submit(handle_client, client_socket, file_reader, search_algorithm, timer)
            futures.append(future)

    except KeyboardInterrupt as e:
        print("Waiting for active threads to finish...")
        for future in futures:
            future.result()  # This will block until the future (thread) has completed.
        print("Socket closed")
        server_socket.close()
        raise e
    finally:
        server_socket.close()

# if __name__ == "__main__":
#     path, ssl_settings = load_config_file()
#     print(type(ssl_settings))
#     search_algorithm = SearchAlgorithms()
#     main(path, ssl_settings, search_algorithm)


            # threads = []  
            # try:  
            # client_thread = threading.Thread(target=handle_client, args=(client_socket, file_reader, search_algorithm, timer))
                # threads.append(client_thread)
            # client_thread.start()
            # finally:
                # for thread in threads:
                #     thread.join()



            # search_value = data.decode().rstrip("\x00")
            # requesting_ip = client_socket.getpeername()[0]
            # current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(f"DEBUG: REREAD_ON_QUERY: {file_reader.reread_on_query}")
            # debug_log = f"DEBUG: Search query: '{(search_value)}', from IP Adress: {requesting_ip}, at: {current_time}"
            # print(debug_log)

            # response = None
            # if file_reader.reread_on_query:
            #     file_contents = file_reader.on_reread_selector()
            #     with lock:
            #         file_contents.sort()
            #     # print(file_contents)
 
            #     file_load_execution_time = timer(1, file_reader.on_reread_selector)
            #     # print("file_load_execution_time:", file_load_execution_time)
            #     sort_exection_time = timer(1, file_contents.sort)
            #     # print("sort_exection_time:",sort_exection_time)
            #     total = file_load_execution_time + sort_exection_time


            # result = search_algorithm.binary_search(file_contents, search_value)
            # search_execution_time = timer(1, search_algorithm.binary_search, file_contents, search_value)

            # if file_reader.reread_on_query:
            #     debug_log = f"DEBUG: The total execution time in ms: {total + search_execution_time:.4f}\n" 
            # else:
            #     debug_log = f"DEBUG: The total execution time minus the time spent on sorting, in ms: {file_load_execution_time + search_execution_time:.4f}\n" 

            # print(debug_log)

            # response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'     
            # client_socket.sendall(response.encode())