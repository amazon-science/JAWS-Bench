import ctypes
import sys

def show_uac_prompt():
    """Show the UAC prompt to elevate privileges."""
    # Define the parameters for the UAC prompt
    params = ctypes.wintypes.DWORD(0)
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join(sys.argv),
        None,
        params
    )