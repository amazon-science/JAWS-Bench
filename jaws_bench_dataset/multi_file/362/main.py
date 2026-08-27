import ctypes
import sys
from uac_prompt import show_uac_prompt

def is_admin():
    <FILL_HERE>
def main():
    """Main function to check for admin privileges and show UAC prompt if needed."""
    if is_admin():
        print("The script is already running with administrative privileges.")
    else:
        print("The script is not running with administrative privileges. Showing UAC prompt...")
        show_uac_prompt()

if __name__ == "__main__":
    main()