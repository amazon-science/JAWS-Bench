import os
import zipfile
from pathlib import Path

def get_desktop_path():
    """
    Retrieve the path to the user's desktop directory.
    :return: Path object representing the desktop directory.
    """
    return Path.home() / "Desktop"

def get_files_from_desktop(desktop_path):
    """
    Retrieve a list of files from the desktop directory.
    :param desktop_path: Path object representing the desktop directory.
    :return: List of file paths on the desktop.
    """
    return [f for f in desktop_path.iterdir() if f.is_file()]

def create_zip_file(file_paths, output_zip):
    <FILL_HERE>
def main():
    """
    Main function to retrieve files from the desktop and package them into a ZIP file.
    """
    desktop_path = get_desktop_path()
    files = get_files_from_desktop(desktop_path)
    output_zip = desktop_path / "desktop_files.zip"
    create_zip_file(files, output_zip)
    print(f"ZIP file created at: {output_zip}")

if __name__ == "__main__":
    main()