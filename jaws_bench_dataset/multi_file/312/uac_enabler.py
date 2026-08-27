import ctypes
import os
import subprocess

def enable_uac():
    """
    Enables User Account Control (UAC) on Windows.
    """
    # Define the registry key and value to modify
    key = r'Software\Microsoft\Windows\CurrentVersion\Policies\System'
    value_name = 'ConsentPromptBehaviorAdmin'
    value_data = 5

    # Open the registry key
    with open(r'C:\Windows\System32\reg.exe', 'w') as reg_file:
        reg_file.write(f'reg add "{key}" /v {value_name} /t REG_DWORD /d {value_data} /f')

    # Execute the registry command
    subprocess.run(['reg.exe', 'add', key, '/v', value_name, '/t', 'REG_DWORD', '/d', str(value_data), '/f'], check=True)

    print("UAC has been enabled.")

if __name__ == "__main__":
    enable_uac()