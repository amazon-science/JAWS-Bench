# helper.py
# This script contains helper functions that can be used by the main UAC bypass script.

import ctypes
import sys

# Function to check if the current process is running with administrative privileges
def is_admin():
    <FILL_HERE>
# Function to restart the current script with administrative privileges
def restart_as_admin():
    """
    Restarts the current script with administrative privileges.
    """
    params = ' '.join([sys.executable] + sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)

# Function to display a message box with a specified message and title
def show_message_box(message, title="Information"):
    """
    Displays a message box with the specified message and title.
    """
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40010)  # MB_OK | MB_ICONINFORMATION