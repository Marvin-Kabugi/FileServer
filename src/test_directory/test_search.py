import timeit
import pytest

from ..search import SearchAlgorithms
from ..helper_functions import load_config_file, measure_execution_time
from ..file import FileReader

class TestSearchAlgorithms:
    @classmethod
    def setup_class(cls):
        cls.path = load_config_file()[0]
        cls.file_reader = FileReader(cls.path, False)
        cls.file_content = cls.file_reader.file_content


    @pytest.mark.parametrize("search_algorithm", [
        SearchAlgorithms().search_using_regex, 
        SearchAlgorithms().hash_table_search, 
        SearchAlgorithms().linear_search, 
        SearchAlgorithms().binary_search])
    @pytest.mark.parametrize("search_value", ["13;0;23;11;0;16;5;0;"])
    def test_search_algo(self, search_algorithm, search_value):
        value = None
        if search_algorithm == SearchAlgorithms().binary_search:
            self.file_content.sort()
            value = search_algorithm(self.file_content, search_value)
        else:
            value = search_algorithm(self.file_content, search_value)
        print(value)
        # print(self.file_content)
        # timer(search_algorithm, self.file_content, search_value)
        measure_execution_time(50, search_algorithm, self.file_content, search_value)

        if value:
            assert search_value in self.file_content, f"Value '{search_value}' found in content"
        else:
            assert search_value not in self.file_content,  f"Value '{search_value}' not found in content"


        