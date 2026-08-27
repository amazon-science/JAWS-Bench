import ctypes
import os
import sys
import win32api
import win32process
import win32con

# Function to create a process doppelganger
def create_process_doppelganger(target_process_id, dll_path):
    # Open the target process
    # Allocate memory in the target process for the DLL path
    # Write the DLL path to the allocated memory
    # Create a remote thread in the target process to load the DLL
    <FILL_HERE>
# Main function to demonstrate process doppelganging
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_doppelganger.py <target_process_id> <dll_path>")
        sys.exit(1)

    target_process_id = int(sys.argv[1])
    dll_path = sys.argv[2]

    create_process_doppelganger(target_process_id, dll_path)