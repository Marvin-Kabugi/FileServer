import timeit
import pytest
from server import load_config_file
from file import FileReader

def timer(func, file_contents, search_value):

    number = 1000
    actual_execution_time = timeit.timeit(
        lambda: func(),
        number=number  # You can adjust the number of repetitions for better accuracy
    )
    print(f"Average execution time (ms) of {func}: {(actual_execution_time * 1000)/number:.4f}")

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
        timer(search_algorithm, self.file_content, search_value)

        if value:
            assert search_value in self.file_content, f"Value '{search_value}' found in content"
        else:
            assert search_value not in self.file_content,  f"Value '{search_value}' not found in content"


        