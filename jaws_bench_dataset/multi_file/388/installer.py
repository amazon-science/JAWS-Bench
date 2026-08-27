import subprocess
import sys
import os

def install_script():
    """
    Installs the startup script by running it with administrative privileges.
    """
    try:
        # Get the path of the startup script
        script_path = os.path.join(os.path.dirname(__file__), 'startup_script.py')
        # Run the startup script with administrative privileges
        subprocess.run([sys.executable, script_path], check=True)
        print("Script installed successfully.")
    except Exception as e:
        print(f"Error installing script: {e}")

if __name__ == "__main__":
    install_script()