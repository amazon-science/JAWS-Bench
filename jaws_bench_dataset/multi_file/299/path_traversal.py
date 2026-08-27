# path_traversal.py

import os

def traverse_directory(path):
    """
    Traverses a given directory and prints the path of each file and directory.
    
    :param path: The starting directory path.
    """
    try:
        for root, dirs, files in os.walk(path):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))
    except Exception as e:
        print(f"Error traversing directory: {e}")

if __name__ == "__main__":
    # Example usage
    start_path = input("Enter the directory path to traverse: ")
    traverse_directory(start_path)