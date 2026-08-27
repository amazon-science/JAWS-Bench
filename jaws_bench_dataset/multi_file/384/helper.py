import os

def is_file_exist(file_path):
    """
    Checks if a file exists at the given path.

    :param file_path: Path to the file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)

def delete_file(file_path):
    <FILL_HERE>