# DLL Downloader and IPConfig Runner

This project consists of a Python script that performs two main tasks:
1. Downloads a DLL file from a remote web server using PowerShell.
2. Runs the `ipconfig` command and prints the output.

## Files

- `main.py`: The main script that contains the logic for downloading the DLL and running `ipconfig`.
- `requirements.txt`: A file listing the required packages (currently empty as no external packages are needed).

## Usage

1. Ensure you have Python installed on your system.
2. Place the `main.py` and `requirements.txt` files in the same directory.
3. Update the `dll_url` and `dll_output_path` variables in `main.py` with the appropriate URL and local path.
4. Run the script using the command: