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
    # messages = ['3;0;1;28;0;7;5;0;', '10;0;1;26;0;8;3;0;', '18;0;6;28;0;23;5;0;']
    messages = ['3;0;1;28;0;7;5;0;', '10;0;1;26;0;8;3;0;', '18;0;6;28;0;23;5;0;', '7;0;1;28;0;9;3;0;', '22;0;6;28;0;23;3;0;', '7;0;6;28;0;23;5;0;', '2;0;1;26;0;7;5;0;', '10;0;1;26;0;7;4;0;', '7;0;1;26;0;8;3;0;', '13;0;1;28;0;7;4;0;']

    response = client.send_message(messages)
    elapsed_time = time.time() - start_time
    print(response)
    time_dict[filename] = elapsed_time

server_exec('10000.txt', 65411)
server_exec('50000.txt', 65445)
server_exec('150000.txt', 65446)
server_exec('250000.txt', 65447)
server_exec('350000.txt', 65448)
server_exec('500000.txt', 65449)
server_exec('750000.txt', 65450)
server_exec('1000000.txt', 65452)

print(time_dict)


