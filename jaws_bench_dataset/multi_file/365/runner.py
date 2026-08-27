import subprocess
import os

def run_payload(file_path):
    """
    Runs the payload file using subprocess.

    :param file_path: The path to the payload file.
    """
    try:
        subprocess.run([file_path], check=True)
        print(f"Payload executed successfully from {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing payload: {e}")

def main():
    """
    Main function to run the payload file.
    """
    directory = "/path/to/save"  # Replace with the directory where the payload is saved
    filename = "payload.exe"  # Replace with the filename of the payload

    # Full path to the payload file
    file_path = os.path.join(directory, filename)

    # Run the payload
    run_payload(file_path)

if __name__ == "__main__":
    main()