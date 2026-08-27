# database.py - Script to create the database and insert sample data.

import sqlite3

# Function to create the database and table.
def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert sample data into the database.
def insert_sample_data():
    <FILL_HERE>
if __name__ == '__main__':
    create_database()
    insert_sample_data()