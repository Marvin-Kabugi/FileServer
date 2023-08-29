import socket
import threading
import os
import ssl
from search import SearchAlgorithms
from file import FileReader
import datetime

from helper_functions import measure_execution_time, load_config_file
from server import main

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 65432
    path, ssl_settings = load_config_file()
    # print(type(ssl_settings))
    search_algorithm = SearchAlgorithms()
    REREAD_ON_QUERY = True
    file = FileReader(path, REREAD_ON_QUERY)
    # print(file.reread_on_query)

    main(path, ssl_settings, search_algorithm, file, measure_execution_time, (HOST, PORT))