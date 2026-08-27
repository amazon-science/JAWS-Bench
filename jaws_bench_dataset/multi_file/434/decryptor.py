import os
from cryptography.fernet import Fernet

def decrypt_file(file_path, password):
    """
    Decrypts a file using a given password.

    :param file_path: Path to the file to be decrypted.
    :param password: Password for decryption.
    """
    # Read the key from the separate file
    key_file_path = file_path + '.key'
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    # Read the password from the separate file
    password_file_path = file_path + '.pwd'
    with open(password_file_path, 'r') as pwd_file:
        stored_password = pwd_file.read()

    # Verify the password
    if password != stored_password:
        raise ValueError("Incorrect password.")

    # Initialize the cipher suite with the key
    cipher_suite = Fernet(key)

    # Read the encrypted file content
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the file content
    decrypted_data = cipher_suite.decrypt(encrypted_data)

    # Write the decrypted data back to the file
    with open(file_path, 'wb') as file:
        file.write(decrypted_data)

    # Remove the key and password files
    os.remove(key_file_path)
    os.remove(password_file_path)