import os
import re
from typing import List

class SearchAlgorithms:
    def binary_search(self, arr: List[str], search_value: str) -> str:
        if arr:
            # arr.sort()
            lower = 0
            higher = len(arr) - 1

            while True:
                if higher < lower:
                    return False
                
                mid_point = lower + ((higher-lower) // 2)

                if arr[mid_point] < search_value:
                    lower = mid_point + 1

                if arr[mid_point] > search_value:
                    higher = mid_point - 1

                if arr[mid_point] == search_value:
                    return True
            

    def linear_search(self, arr: List[str], search_value: str) -> str:
        if arr:
            for line in arr:
                if line.strip() == search_value:
                    return True
        return False

        

    def search_using_regex(self, arr: List[str], search_value: str) -> str:
        if arr:
            for line in arr:
                if re.fullmatch(f'^{search_value}$', line.strip()):
                    return True
            return False

        
    
    def hash_table_search(self, arr: List[str], search_value: str) -> str:
        if arr:
            hash_table = {}

            for (key, value) in enumerate(arr):
                hash_table[value] = key
            
            if search_value in hash_table:
                return True
        
        return False
        
        
    def grep_search(path: str, search_value: str):
        command = f"grep ^{search_value}$ {path}"
        value = os.system(command)
        print(value)