import timeit
import os


def measure_execution_time(number, func, *args):
    if callable(func):
        actual_execution_time = timeit.timeit(lambda: func(*args), number=number)
    else:
        actual_execution_time = timeit.timeit(func, number=number)

    # print(f"Average execution time in(ms): {(actual_execution_time * 1000)/number:.4f}")
    return ((actual_execution_time * 1000)/number)


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
    script_directory = os.getcwd()
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
        except FileNotFoundError as e:
            print("File not found")
            raise e
    if required_path is None:
        print("No path found in the config file")
    else:
        data_path = required_path
        return (data_path, ssl_settings)
    

def load_test_file() -> str:
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
    script_directory = os.getcwd()
    config = os.path.join(script_directory, 'config.txt')
    test_directory = os.path.join(script_directory, 'Files')
    ssl_settings = None
    if os.path.exists(config):
        try:
            with open(config, 'r') as con:
                for line in con:
                    if line.startswith("SSL="):
                        ssl_settings = line.strip().split("=")[1]
        except FileNotFoundError as e:
            print("File not found")
            raise e
    if test_directory is None:
        print("No path found in the config file")
    else:
    
        return (test_directory, ssl_settings)  

def load_test_files() -> str:
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
    script_directory = os.getcwd()
    config = os.path.join(script_directory, 'config.txt')
    test_directory = os.path.join(script_directory, 'Files')
    test_files = []
    for filename in os.listdir(test_directory):
        if os.path.isfile(os.path.join(test_directory, filename)):
            test_files.append(os.path.join(test_directory, filename))
    # print(test_files)

    # required_path = None
    ssl_settings = None
    if os.path.exists(config):
        try:
            with open(config, 'r') as con:
                for line in con:
                    # if line.startswith("linuxpath="):
                    #     required_path = line.strip().split('=')[1]
                    if line.startswith("SSL="):
                        ssl_settings = line.strip().split("=")[1]
        except FileNotFoundError as e:
            print("File not found")
            raise e
    # data_path = required_path
    return (test_files, ssl_settings)