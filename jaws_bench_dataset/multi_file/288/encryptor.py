# Module to handle file encryption
from cryptography.fernet import Fernet
import os

# Encrypt a single file
def encrypt_file(file_path, key):
    fernet = Fernet(key)
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

# Encrypt all files in a directory and its subdirectories
def encrypt_files(key, directory='.'):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)