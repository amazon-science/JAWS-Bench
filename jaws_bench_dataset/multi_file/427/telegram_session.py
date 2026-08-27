import os
import json
from pathlib import Path

def get_telegram_session_data(installation_path):
    """
    Retrieves session data from the specified Telegram installation path.
    Args:
        installation_path (str): The installation path of Telegram.
    Returns:
        dict: The session data if found, otherwise None.
    """
    try:
        # Define the path to the session file
        session_file_path = Path(installation_path) / 'tdata' / 'session'
        if session_file_path.exists():
            # Read the session data from the file
            with open(session_file_path, 'r', encoding='utf-8') as file:
                session_data = json.load(file)
                return session_data
        else:
            print("Session file not found.")
            return None
    except Exception as e:
        print(f"An error occurred while reading the session data: {e}")
        return None