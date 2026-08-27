import ctypes
from ctypes import wintypes

# Define necessary constants and structures
SYSTEM_MODULE_INFORMATION = 11
NTSTATUS = wintypes.LONG

class SYSTEM_MODULE_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("Reserved1", wintypes.PVOID),
        ("Reserved2", wintypes.PVOID),
        ("ImageBase", wintypes.PVOID),
        ("ImageSize", wintypes.ULONG),
        ("Flags", wintypes.ULONG),
        ("LoadOrderIndex", wintypes.WORD),
        ("InitOrderIndex", wintypes.WORD),
        ("LoadCount", wintypes.WORD),
        ("ModuleNameOffset", wintypes.WORD),
        ("ImageName", wintypes.CHAR * 256),
        ("Next", ctypes.POINTER(SYSTEM_MODULE_INFORMATION)),
    ]

# Load the kernel32.dll
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# Define the NtQuerySystemInformation function
NtQuerySystemInformation = kernel32.NtQuerySystemInformation
NtQuerySystemInformation.argtypes = [wintypes.ULONG, wintypes.PVOID, wintypes.ULONG, wintypes.PULONG]
NtQuerySystemInformation.restype = NTSTATUS