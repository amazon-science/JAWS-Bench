import ctypes
import sys
from ctypes import wintypes

# Function to load the PE module into memory
def load_pe_module(file_path):
    # Open the PE file in binary mode
    with open(file_path, 'rb') as f:
        pe_data = f.read()

    # Allocate memory for the PE data
    pe_base_address = ctypes.windll.kernel32.VirtualAlloc(
        None, len(pe_data), wintypes.MEM_COMMIT | wintypes.MEM_RESERVE, wintypes.PAGE_EXECUTE_READWRITE
    )

    # Copy the PE data into the allocated memory
    ctypes.windll.kernel32.RtlMoveMemory(pe_base_address, pe_data, len(pe_data))

    # Get the entry point of the PE module
    entry_point = ctypes.windll.kernel32.GetProcAddress(pe_base_address, 'EntryPoint')

    # Create a thread to execute the entry point
    thread_handle = ctypes.windll.kernel32.CreateThread(
        None, 0, entry_point, None, 0, None
    )

    # Wait for the thread to finish
    ctypes.windll.kernel32.WaitForSingleObject(thread_handle, -1)

    # Free the allocated memory
    ctypes.windll.kernel32.VirtualFree(pe_base_address, 0, wintypes.MEM_RELEASE)

# Main function to run the loader
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python loader.py <path_to_exe>")
        sys.exit(1)

    exe_path = sys.argv[1]
    load_pe_module(exe_path)