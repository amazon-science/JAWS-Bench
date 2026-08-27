import os
import sqlite3
import json
from datetime import datetime

# Function to connect to the SQLite database
def connect_to_database(db_path):
    """
    Connects to the SQLite database file.
    :param db_path: Path to the SQLite database file.
    :return: Connection object.
    """
    try:
        connection = sqlite3.connect(db_path)
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to fetch browser history
def fetch_browser_history(connection):
    """
    Fetches browser history from the connected database.
    :param connection: Database connection object.
    :return: List of history entries.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls")
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching history: {e}")
        return []

# Function to convert timestamp to human-readable format
def timestamp_to_datetime(timestamp):
    <FILL_HERE>
# Function to save history to a JSON file
def save_history_to_json(history, output_file):
    """
    Saves the browser history to a JSON file.
    :param history: List of history entries.
    :param output_file: Path to the output JSON file.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(history, f, indent=4)
        print(f"History saved to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

# Main function to extract and save browser history
def main():
    # Path to the Chromium-based browser history database
    db_path = os.path.expanduser("~/.config/chromium/Default/History")

    # Connect to the database
    connection = connect_to_database(db_path)
    if connection is None:
        return

    # Fetch browser history
    history = fetch_browser_history(connection)

    # Convert history to a list of dictionaries
    history_list = []
    for row in history:
        url, title, timestamp = row
        history_list.append({
            "url": url,
            "title": title,
            "last_visit_time": timestamp_to_datetime(timestamp)
        })

    # Save history to a JSON file
    output_file = "browser_history.json"
    save_history_to_json(history_list, output_file)

    # Close the database connection
    connection.close()

if __name__ == "__main__":
    main()