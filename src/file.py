from typing import List
import re

class FileReader:
    def __init__(self, path: str, reread_on_query: bool) -> None:
        self.path = path
        self.reread_on_query = reread_on_query
        self.file_content = self._read_file()

    
    def _read_file(self):
        try:
            with open(self.path, "r") as file:
                print("opening")
                read_file = [line.strip() for line in file.readlines()]
                # print(read_file)
                return read_file
            
        except FileNotFoundError as e:
            return e
    
        
    def on_reread_selector(self):
        if self.reread_on_query:
            self.file_content = self._read_file()
        
        return self.file_content


