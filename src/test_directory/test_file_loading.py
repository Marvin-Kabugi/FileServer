import pytest
import os

from ..file import FileReader
from ..helper_functions import load_config_file

path = load_config_file()[0]

with open(path, 'r') as file:
    content = file.readlines()

class TestFileReader:
    def test_read_file(self):
        file_reader = FileReader(path, False)

        file_content = file_reader._read_file()
        assert(file_content is not None)
        assert(file_content == [line.strip() for line in content])

    def test_read_file_mmap(self):
        '''Hey'''
        file_reader = FileReader(path, False)

        file_content = file_reader._read_file_mmap()
        assert(file_content is not None)
        assert([line.strip() for line in file_content] == [line.strip() for line in content])

    
    def test_read_file_with_mmap_list(self):
        file_reader = FileReader(path, False)

        file_content = file_reader._read_file_with_mmap_list()
        assert(file_content is not None)
        assert(file_content == [line.strip() for line in content])


    # Test case for _read_file method with FileNotFoundError
    def test_read_file_file_not_found(self):
        # Initialize FileReader with a non-existent file
        file_reader = FileReader(os.path.join(os.getcwd(), 'src','fil.py'), False)

        # Check if _read_file method raises FileNotFoundError
        with pytest.raises(FileNotFoundError):
            file_reader._read_file()


    # Test case for _read_file_mmap method with FileNotFoundError
    def test_read_file_mmap_file_not_found(self):
        # Initialize FileReader with a non-existent file
        file_reader = FileReader(os.path.join(os.getcwd(), 'src','fil.py'), False)

        # Check if _read_file_mmap method raises FileNotFoundError
        with pytest.raises(FileNotFoundError):
            file_reader._read_file_mmap()


    def test_read_file_with_mmap_list_not_found(self):
        # Initialize FileReader with a non-existent file
        file_reader = FileReader(os.path.join(os.getcwd(), 'src','fil.py'), False)

        # Check if _read_file_mmap method raises FileNotFoundError
        with pytest.raises(FileNotFoundError):
            file_reader._read_file_with_mmap_list()

