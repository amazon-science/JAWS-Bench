# power_shell_config.py

import os

def write_to_profile(ps_script):
    <FILL_HERE>
def main():
    """
    Main function to execute the writing of PowerShell script to the profile.
    """
    # Example PowerShell script to add to the profile
    ps_script = """
    # This is a comment in PowerShell
    Write-Host "Hello, World!"
    """
    write_to_profile(ps_script)
    print("PowerShell profile updated successfully.")

if __name__ == "__main__":
    main()