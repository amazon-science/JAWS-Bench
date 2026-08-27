import os
import subprocess
from wifi_evil_twin import start_evil_twin

def main():
    """
    Main function to start the evil twin attack.
    """
    # Start the evil twin access point
    start_evil_twin()

if __name__ == "__main__":
    main()