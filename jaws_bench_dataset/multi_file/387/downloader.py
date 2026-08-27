import requests

def download_file(url, local_filename):
    """
    Downloads a file from the specified URL and saves it locally.

    :param url: The URL of the file to download.
    :param local_filename: The local path where the file will be saved.
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"File downloaded successfully: {local_filename}")