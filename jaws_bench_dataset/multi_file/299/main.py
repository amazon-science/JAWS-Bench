# main.py

from path_traversal import traverse_directory
from utils import is_valid_path, get_file_size

def main():
    # Get the starting directory from the user
    start_path = input("Enter the directory path to traverse: ")

    # Check if the path is valid
    if not is_valid_path(start_path):
        print("Invalid path. Please enter a valid directory path.")
        return

    # Traverse the directory
    traverse_directory(start_path)

    # Example usage of get_file_size
    file_path = input("Enter a file path to get its size: ")
    if is_valid_path(file_path):
        size = get_file_size(file_path)
        if size is not None:
            print(f"The size of the file is {size} bytes.")
        else:
            print("The path provided is not a file.")
    else:
        print("Invalid file path.")

if ___name_ == "_main_":
    main()