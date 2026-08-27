import ctypes
from ctypes import wintypes

# Load necessary Windows API functions
kernel32 = ctypes.WinDLL('kernel32')

# Define necessary constants
PROCESS_ALL_ACCESS = 0x001F0FFF
THREAD_ALL_ACCESS = 0x001F03FF
MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PAGE_READWRITE = 0x04

def inject_dll(target_process_id, dll_path):
    # Open the target process
    target_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target_process_id)
    if not target_process:
        raise ctypes.WinError()

    # Get the address of LoadLibraryA in kernel32.dll
    load_library_addr = kernel32.GetProcAddress(kernel32.GetModuleHandleW("kernel32.dll"), "LoadLibraryA")

    # Allocate memory in the target process for the DLL path
    dll_path_bytes = dll_path.encode('utf-8')
    allocated_memory = kernel32.VirtualAllocEx(target_process, None, len(dll_path_bytes) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)
    if not allocated_memory:
        raise ctypes.WinError()

    # Write the DLL path to the allocated memory
    written_bytes = ctypes.c_size_t()
    if not kernel32.WriteProcessMemory(target_process, allocated_memory, dll_path_bytes, len(dll_path_bytes) + 1, ctypes.byref(written_bytes)):
        raise ctypes.WinError()

    # Create a remote thread in the target process to call LoadLibraryA with the DLL path
    thread_id = ctypes.c_size_t()
    remote_thread = kernel32.CreateRemoteThread(target_process, None, 0, load_library_addr, allocated_memory, 0, ctypes.byref(thread_id))
    if not remote_thread:
        raise ctypes.WinError()

    # Wait for the remote thread to finish
    kernel32.WaitForSingleObject(remote_thread, -1)

    # Close handles
    kernel32.CloseHandle(remote_thread)
    kernel32.CloseHandle(target_process)

# Example usage
if __name__ == "__main__":
    target_process_id = 1234  # Replace with the actual target process ID
    dll_path = "C:\\path\\to\\your\\dll.dll"  # Replace with the actual DLL path

    inject_dll(target_process_id, dll_path)