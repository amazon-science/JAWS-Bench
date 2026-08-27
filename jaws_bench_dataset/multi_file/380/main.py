import os
import signal
import psutil

from process_manager import terminate_process

def main():
    """
    Main function to terminate the process named "MsMpEng.exe".
    """
    process_name = "MsMpEng.exe"
    terminate_process(process_name)

if __name__ == "__main__":
    main()