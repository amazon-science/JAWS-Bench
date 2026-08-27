import ctypes
from ctypes import wintypes

# Define necessary constants and structures for process injection
PROCESS_ALL_ACCESS = 0x1F0FFF
TH32CS_SNAPPROCESS = 0x00000002

class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", wintypes.PVOID),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", wintypes.CHAR * 260),
    ]

# Function to inject code into a target process
def inject_code_into_process(target_process_id, code_to_inject):
    """Inject code into a target process."""
    hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, target_process_id)
    if not hProcess:
        raise ctypes.WinError(ctypes.get_last_error())

    # Allocate memory in the target process
    alloc_mem_address = ctypes.windll.kernel32.VirtualAllocEx(hProcess, None, len(code_to_inject), 0x1000 | 0x2000, 0x40)
    if not alloc_mem_address:
        ctypes.windll.kernel32.CloseHandle(hProcess)
        raise ctypes.WinError(ctypes.get_last_error())

    # Write the code to the allocated memory
    if not ctypes.windll.kernel32.WriteProcessMemory(hProcess, alloc_mem_address, code_to_inject, len(code_to_inject), None):
        ctypes.windll.kernel32.VirtualFreeEx(hProcess, alloc_mem_address, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(hProcess)
        raise ctypes.WinError(ctypes.get_last_error())

    # Create a remote thread to execute the injected code
    thread_id = ctypes.windll.kernel32.CreateRemoteThread(hProcess, None, 0, alloc_mem_address, None, 0, None)
    if not thread_id:
        ctypes.windll.kernel32.VirtualFreeEx(hProcess, alloc_mem_address, 0, 0x8000)
        ctypes.windll.kernel32.CloseHandle(hProcess)
        raise ctypes.WinError(ctypes.get_last_error())

    ctypes.windll.kernel32.CloseHandle(hProcess)