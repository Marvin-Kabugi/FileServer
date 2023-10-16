import os
import time
import pytest
import threading

from search import SearchAlgorithms
from helper_functions import load_test_file, measure_execution_time
from server import main
from client import Client
from file import FileReader


REREAD_ON_QUERY = True
time_dict = {}

def server_exec(filename, port):
    HOST = "127.0.0.1"
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, filename)
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, port)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, port)
    start_time = time.time()
    # client.send_message('4;0;1;28;0;5;3;0;\x00')
    messages = ['3;0;1;28;0;7;5;0;', '10;0;1;26;0;8;3;0;', '18;0;6;28;0;23;5;0;']

    response = client.send_message(messages)
    elapsed_time = time.time() - start_time
    print(f'The response outside the loop: {response}')
    while True:
        if "STRING NOT FOUND" not in response:
            break
        messages = messages.pop()
        print(f'Messages inside the loop {messages}')
        start_time = time.time()
        response = client.send_message(messages)
        print(f'The response inside the loop: {response}')
        elapsed_time = time.time() - start_time

    time_dict[filename] = elapsed_time
    print(f'The length of messages is {len(messages)}')
    qps = len(messages)/elapsed_time
    print(f'The queries per second of {filename} is:', qps)

server_exec('10000.txt', 65411)
server_exec('50000.txt', 65445)
server_exec('150000.txt', 65446)
server_exec('250000.txt', 65447)
server_exec('350000.txt', 65448)
server_exec('500000.txt', 65449)
server_exec('750000.txt', 65450)
server_exec('1000000.txt', 65452)

print(time_dict)


# import os
# import time
# import pytest
# import threading

# from search import SearchAlgorithms
# from helper_functions import load_test_file, measure_execution_time
# from server import main
# from client import Client
# from file import FileReader

# REREAD_ON_QUERY = True
# time_dict = {}

# def server_exec(filename, port):
#     HOST = "127.0.0.1"
#     search_algorithm = SearchAlgorithms()
#     path, ssl_settings = load_test_file()
#     path = os.path.join(path, filename)
#     file = FileReader(path, REREAD_ON_QUERY)

#     # Start the server in a separate thread
#     server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, port)))
#     server.start()
#     # Wait for the server to start
#     time.sleep(3)
    
#     client = Client(HOST, port)

#     messages = ['3;0;1;28;0;7;5;0;', '10;0;1;26;0;8;3;0;', '18;0;6;28;0;23;5;0;']

#     start_time = time.time()

#     total_queries_sent = 0
#     for message in messages:
#         response = client.send_message(message)
#         print('This is the response:',response)
#         if "STRING NOT FOUND" in response:
#             break
#         print('In loop',message)
#         total_queries_sent += 1

#     elapsed_time = time.time() - start_time

#     time_dict[filename] = elapsed_time

#     # Calculating QPS
#     qps = total_queries_sent / elapsed_time
#     print(f'The queries per second of {filename} is:', qps)
