import os
import re
from typing import List

class SearchAlgorithms:
    def binary_search(self, arr: List[str], search_value: str) -> str:
        arr.sort()
        lower = 0
        higher = len(arr) - 1

        while True:
            if higher < lower:
                return ("STRING NOT FOUND\n")
            
            mid_point = lower + ((higher-lower) // 2)

            if arr[mid_point] < search_value:
                lower = mid_point + 1

            if arr[mid_point] > search_value:
                higher = mid_point - 1

            if arr[mid_point] == search_value:
                return ("STRING EXISTS\n")
        

    def linear_search(self, arr: List[str], search_value: str) -> str:
        try:
            for line in arr:
                if line.strip() == search_value:
                    return ("STRING EXISTS\n")
            return ("STRING NOT FOUND\n")
        except Exception as e:
            return e
        

    def search_using_regex(self, arr: List[str], searchvalue: str) -> str:
        try:
            for line in arr:
                if re.fullmatch(f'^{searchvalue}$', line.strip()):
                    return ("STRING EXISTS\n")
            return ("STRING NOT FOUND\n")
        except Exception as e:
            return e
        
        
    def grep_search(path: str, search_value: str):
        command = f"grep ^{search_value}$ {path}"
        os.system(command)











# def load_files(path: str) -> str:
#     try:
#         with open(path, "r") as file:
#                 lines = file.readlines()
#                 lines = [line.strip() for line in lines]
#                 filtered_lines = filter_duplicates(lines)
#                 # for line in filtered_lines:
#                 #     yield line
#                 yield filtered_lines
#     except FileNotFoundError:
#         print("File not found")
    
    
# def load_config_file():
#     script_directory = os.path.dirname(os.path.abspath(__file__))
#     config = os.path.join(script_directory, 'config.txt')
#     # config = os.path.join('src', 'config.txt')
#     required_path = None
#     # print(config)
#     if os.path.exists(config):
#         try:
#             with open(config, 'r') as con:
#                 for line in con:
#                     if line.startswith("linuxpath="):
#                         required_path = line.strip().split('=')[1]
#                         break
#         except FileNotFoundError:
#             print("File not found")
#     if required_path is None:
#         print("No path found in the config file")
#     else:
#         data_path = required_path
#         # for line in load_files(data_path):
#         #     print(line)
#         # print(next(load_files(data_path)))
#         print(binary_search(next(load_files(data_path)), "18;0;1;11;0;7;3;0;"))
#         print(linear_search(data_path, "18;0;1;11;0;7;3;0;"))
#         print(search_using_regex(data_path, "18;0;1;11;0;7;3;0;"))

# load_config_file()


        


# def binary_search(arr: List[str], search_value: str) -> str:
#     arr.sort()
#     lower = 0
#     higher = len(arr) - 1

#     while True:
#         if higher < lower:
#             return ("Search value does not exist")
        
#         mid_point = lower + ((higher-lower) // 2)

#         if arr[mid_point] < search_value:
#             lower = mid_point + 1

#         if arr[mid_point] > search_value:
#             higher = mid_point - 1
#         if arr[mid_point] == search_value:
#             return ("Exists")
        
# def linear_search(path: str, search_value: str) -> str:
#     try:
#         with open(path, 'r') as file:
#             for line in file:
#                 if line.strip() == search_value:
#                     return ("STRING EXISTS\n")
#             return ("STRING NOT FOUND\n")
#     except FileNotFoundError as e:
#         return ("File does not Exist")
    
# def search_using_regex(path: str, searchvalue: str) -> str:
#     try:
#         with open(path, 'r') as file:
#             for line in file:
#                 if re.fullmatch(f'^{searchvalue}$', line.strip()):
#                     return ("STRING EXISTS\n")
#             return ("STRING NOT FOUND\n")
#     except FileNotFoundError as e:
#         return ("File does not Exist")
    
# def grep_search(path: str, search_value: str):
#     command = f"grep ^{search_value}$ {path}"
#     os.system(command)