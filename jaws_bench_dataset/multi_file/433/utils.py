import os
from pathlib import Path

def is_valid_file(file_path):
    """
    Checks if the given file path is valid and is a regular file.

    Args:
        file_path (Path): The path to the file to check.

    Returns:
        bool: True if the file is valid, False otherwise.
    """
    return file_path.is_file()

def get_all_files(directory_path):
    """
    Gets all valid files in the given directory.

    Args:
        directory_path (Path): The path to the directory.

    Returns:
        list: A list of valid file paths.
    """
    files = []
    for item in directory_path.iterdir():
        if is_valid_file(item):
            files.append(item)
    return files