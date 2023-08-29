import os
import time
import pytest
import threading

from ..search import SearchAlgorithms
from ..helper_functions import load_test_file, measure_execution_time
from ..server import main
from ..client import Client
from ..file import FileReader

    
REREAD_ON_QUERY = False
server_lock = threading.Lock()

def test_10000_txt():
    HOST = "127.0.0.1"
    PORT = 65453
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '10000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content)
    print(sm)

  
def test_50000_txt():
    HOST = "127.0.0.1"
    PORT = 65454
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '50000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)

            # Wait for the server thread to complete
        # print(len(sm))
        # assert sm == ("STRING EXISTS\n" * 2)

 


def test_150000_txt():
    HOST = "127.0.0.1"
    PORT = 65455
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '150000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)


  


def test_250000_txt():
    HOST = "127.0.0.1"
    PORT = 65456
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '250000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)






def test_350000_txt():
    HOST = "127.0.0.1"
    PORT = 65457
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '350000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)







def test_500000_txt():
    HOST = "127.0.0.1"
    PORT = 65458
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '500000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)





def test_750000_txt():
    HOST = "127.0.0.1"
    PORT = 65459
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '750000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)






def test_1000000_txt():
    HOST = "127.0.0.1"
    PORT = 65460
    search_algorithm = SearchAlgorithms()
    path, ssl_settings = load_test_file()
    path = os.path.join(path, '1000000.txt')
    print(path)
    file = FileReader(path, REREAD_ON_QUERY)

    # Start the server in a separate thread
    server = threading.Thread(target=main, args=(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT)))
    server.start()
    # Wait for the server to start
    time.sleep(3)
    # Run the client logic in the main thread
    client = Client(HOST, PORT)
    sm = client.send_message(file.file_content[:4])
    print(sm)


    
