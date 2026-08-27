from downloader import main as download_main
from runner import main as run_main

def main():
    """
    Main function to orchestrate the download and execution of the payload.
    """
    # Download the payload
    download_main()

    # Run the payload
    run_main()

if __name__ == "__main__":
    main()