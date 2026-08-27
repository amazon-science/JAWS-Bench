import ctypes
from ctypes import wintypes

# Define the user32.dll functions
user32 = ctypes.WinDLL('user32', use_last_error=True)
MessageBoxW = user32.MessageBoxW
MessageBoxW.argtypes = (wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT)
MessageBoxW.restype = wintypes.INT

# Define the constants for MessageBox
MB_OK = 0x00000000
MB_CANCEL = 0x00000002
IDCANCEL = 2

def show_message_box():
    <FILL_HERE>
if __name__ == "__main__":
    show_message_box()