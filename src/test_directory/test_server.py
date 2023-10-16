import pytest
from unittest.mock import Mock
# from ..src.server import handle_client, main, extract_element
from .. import server
import sys
# print('feghjkjh ',sys.path)
@pytest.fixture
def mock_setup():
    mock_socket = Mock()
    mock_socket.recv.side_effect = [b"sample_input_data\x00", b""]
    mock_socket.getpeername.return_value = ('127.0.0.1', 12345)

    mock_file_reader = Mock()
    mock_file_reader.file_content = ["test_data"]
    mock_file_reader.reread_on_query = False

    mock_search_algorithm = Mock()
    mock_search_algorithm.binary_search.return_value = True  # Assume binary search finds the data

    mock_timer = Mock()
    mock_timer.return_value = 1.0

    return mock_socket, mock_file_reader, mock_search_algorithm, mock_timer

def test_handle_client_success(mock_setup, mocker):
    mock_socket, mock_file_reader, mock_search_algorithm, mock_timer = mock_setup

    mocker.patch('src.server.print')  # To suppress print calls
    server.handle_client(mock_socket, mock_file_reader, mock_search_algorithm, mock_timer)
    mock_socket.sendall.assert_called_with(b"STRING EXISTS\n")

def test_extract_element_success():
    input_data = "data1;data2;data3;data4;data5;data6;data7;data8;"
    expected_element = "data1;data2;data3;data4;data5;data6;data7;data8;"
    element, remaining_buffer, flag = server.extract_element(input_data)
    assert element == expected_element
    assert flag

def test_extract_element_incomplete():
    input_data = "data1;data2;"
    element, remaining_buffer, flag = server.extract_element(input_data)
    assert element is None
    assert not flag

def test_handle_client_reread_on_query_true(mock_setup, mocker):
    mock_socket, mock_file_reader, mock_search_algorithm, mock_timer = mock_setup
    mock_file_reader.reread_on_query = True

    mocker.patch('src.server.print')  # To suppress print calls
    server.handle_client(mock_socket, mock_file_reader, mock_search_algorithm, mock_timer)
    mock_socket.sendall.assert_called_with(b"STRING EXISTS\n")



# You might want to add more tests such as testing socket errors, testing the binary_search behavior, and any other logic you have in the main code.
