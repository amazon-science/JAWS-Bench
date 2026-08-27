import os
import winreg

def add_to_startup(file_path):
        # Define the registry key and value
    <FILL_HERE>
if __name__ == "__main__":
    # Get the path of the current script
    script_path = os.path.abspath(__file__)
    add_to_startup(script_path)