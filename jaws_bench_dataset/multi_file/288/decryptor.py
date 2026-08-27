# Module to handle file decryption
from cryptography.fernet import Fernet
import os

# Decrypt a single file
def decrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted)

# Decrypt all files in a directory and its subdirectories
def decrypt_files(key, directory='.'):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)