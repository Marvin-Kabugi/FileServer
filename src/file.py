from typing import List
import mmap


class FileReader:
    """
    A utility class for reading and managing file content.

    This class allows you to read the content of a file, store it internally, and optionally reread the content
    upon request. It provides methods to initialize the file reader, read the file content, and trigger a reread
    if needed.

    Args:
        path (str): The path to the file to be read.
        reread_on_query (bool): If True, the file content will be reread from the file each time the
            `on_reread_selector` method is called.

    Attributes:
        path (str): The path to the file.
        reread_on_query (bool): Flag indicating whether rereading the file content on query is enabled.
        file_content (List[str] or FileNotFoundError): The content of the file as a list of lines, or an instance
            of FileNotFoundError if the file doesn't exist.

    Methods:
        __init__(self, path: str, reread_on_query: bool) -> None:
            Initializes the FileReader instance with the given file path and reread configuration.

        _read_file(self):
            Reads the content of the file located at the specified path.

        _read_file_mmap(self):
            Reads the content of the file located at the specified path.

        on_reread_selector(self):
            Returns the stored file content. If reread_on_query is True, this method will reread the file and
            update the stored content.
    """
    def __init__(self, path: str, reread_on_query: bool) -> None:
        self.path = path
        self.reread_on_query = reread_on_query
        self.file_content = self._read_file_mmap()

    
    def _read_file(self):
        try:
            with open(self.path, "r") as file:
                # print("opening")
                return [line.strip() for line in file.readlines()]
            
        except FileNotFoundError as e:
            raise e
    
    def _read_file_mmap(self) -> List[str]:
        """
        Reads the file using memory-mapped I/O for efficient access.
        
        Returns:
        list: Contents of the file split into lines.
        
        Raises:
        FileNotFoundError: If the file at the specified path is not found.
        """
        try:
            with open(self.path, 'r') as file:
                # print("opening")
                with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    content = mmapped_file.read()
                    return content.decode().strip().split('\r\n')
        except FileNotFoundError as e:
            raise e
        

    def _read_file_with_mmap_list(self) -> List[str]:
        try:
            with open(self.path, "r") as file:
                # print("opening")
                with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                    lines = []
                    start = 0
                    while start < len(mmapped_file):
                        end = mmapped_file.find(b'\n', start)
                        if end == -1:
                            end = len(mmapped_file)
                        line_bytes = mmapped_file[start:end]
                        line = line_bytes.decode()
                        lines.append(line.strip())
                        start = end + 1
            return lines
        
        except FileNotFoundError as e:
            raise e


        
    def on_reread_selector(self) -> List[str]:
        """
        Get the stored file content.

        Returns:
            List[str] or FileNotFoundError: The stored file content as a list of lines, or an instance of
                FileNotFoundError if the file doesn't exist. If reread_on_query is True, the file content
                will be reread from the file before being returned.
        """
        if self.reread_on_query:
            self.file_content = self._read_file_mmap()
        
        return self.file_content


