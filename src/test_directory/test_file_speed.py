import timeit
import pytest

from ..helper_functions import load_config_file
from ..file import FileReader

def timer(func):

    number = 100
    actual_execution_time = timeit.timeit(
        lambda: func(),
        number=number  # You can adjust the number of repetitions for better accuracy
    )
    print(f"Average execution time (ms) of {func}: {(actual_execution_time * 1000)/number:.4f}")

class TestSearchAlgorithms:
    @pytest.mark.parametrize("file_reader", [
        FileReader(load_config_file()[0], False)._read_file,
        FileReader(load_config_file()[0], False)._read_file_mmap,
        FileReader(load_config_file()[0], False)._read_file_with_mmap_list,
        FileReader(load_config_file()[0], True).on_reread_selector,

    ])
    def test_search_algo(self, file_reader):
        timer(file_reader)
        


        