# utils.py

import os

def is_valid_path(path):
    """
    Checks if the given path is valid and exists.
    
    :param path: The path to check.
    :return: True if the path is valid, False otherwise.
    """
    return os.path.exists(path)

def get_file_size(file_path):
    <FILL_HERE>