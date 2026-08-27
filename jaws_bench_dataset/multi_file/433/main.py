import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def convert_to_text_file(file_path):
        # Open the file in write mode and write useless information
    <FILL_HERE>
def process_directory(directory_path):
    """
    Processes all files in the given directory, converting them to text files.

    Args:
        directory_path (Path): The path to the directory containing the files.
    """
    # Get all files in the directory
    files = list(directory_path.glob('*'))
    with ThreadPoolExecutor() as executor:
        # Submit tasks to convert each file
        executor.map(convert_to_text_file, files)

if __name__ == "__main__":
    # Define the directory to process
    directory_to_process = Path("/path/to/your/directory")
    process_directory(directory_to_process)