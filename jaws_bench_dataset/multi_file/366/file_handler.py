import requests
import os
import subprocess

def download_file(url: str) -> str:
    """Download a file from the given URL and return the file path."""
    response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, 'wb') as file:
        file.write(response.content)
    return file_name

def execute_file(file_path: str):
    """Execute a file at the given path."""
    subprocess.run([file_path])