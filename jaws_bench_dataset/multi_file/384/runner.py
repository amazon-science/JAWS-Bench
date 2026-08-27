import os
import sys
from helper import is_file_exist, delete_file

def main():
    """
    Main function to execute the script removal process.
    """
    # Get the path of the main script
    main_script_path = os.path.abspath('main.py')

    # Check if the main script exists
    if is_file_exist(main_script_path):
        # Remove the main script
        delete_file(main_script_path)
    else:
        print(f"Main script {main_script_path} does not exist.")

if __name__ == "__main__":
    # Call the main function
    main()