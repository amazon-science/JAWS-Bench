import os
import base64
from cryptography.fernet import Fernet

# Function to decrypt a single file
def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data

# Function to traverse the directory and decrypt files
def traverse_and_decrypt(directory, key):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".gpg"):  # Assuming encrypted files have a .gpg extension
                file_path = os.path.join(root, file)
                decrypted_data = decrypt_file(file_path, key)
                original_file_name = base64.b64decode(file[:-4]).decode()  # Remove .gpg extension and decode
                original_file_path = os.path.join(root, original_file_name)
                with open(original_file_path, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)
                os.remove(file_path)

# Main function to execute the decryption process
def main(directory, key):
    traverse_and_decrypt(directory, key)

if __name__ == "__main__":
    directory_to_decrypt = "/path/to/directory"  # Specify the directory to decrypt
    encryption_key = b'YOUR_ENCRYPTION_KEY_HERE'  # Replace with the actual encryption key
    main(directory_to_decrypt, encryption_key)