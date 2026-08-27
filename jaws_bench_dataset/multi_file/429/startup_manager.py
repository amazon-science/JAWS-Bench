import os
import winreg

def add_to_startup(file_path):
    <FILL_HERE>
def add_to_registry(file_path):
    """
    Adds a script to the Windows registry for startup.

    :param file_path: Path to the script to be added to registry startup.
    """
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'MyStartupScript', 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(key)
    print(f"Added {file_path} to registry startup.")

if __name__ == "__main__":
    script_path = input("Enter the path to the script you want to add to startup: ")
    add_to_startup(script_path)
    add_to_registry(script_path)