import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, password):
    """
    Encrypts a file using a given password.

    :param file_path: Path to the file to be encrypted.
    :param password: Password for encryption.
    """
    # Generate a key from the password
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Read the file content
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Encrypt the file content
    encrypted_data = cipher_suite.encrypt(file_data)

    # Write the encrypted data back to the file
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

    # Save the key to a separate file
    key_file_path = file_path + '.key'
    with open(key_file_path, 'wb') as key_file:
        key_file.write(key)

    # Save the password to a separate file
    password_file_path = file_path + '.pwd'
    with open(password_file_path, 'w') as pwd_file:
        pwd_file.write(password)