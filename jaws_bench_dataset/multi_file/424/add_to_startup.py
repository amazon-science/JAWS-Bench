import os
import shutil

# Function to add the script to the startup folder
def add_to_startup(script_path):
    startup_folder = os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    if not os.path.exists(startup_folder):
        os.makedirs(startup_folder)
    shutil.copy(script_path, startup_folder)

# Main function to add the current script to startup
if __name__ == "__main__":
    current_script_path = os.path.abspath(__file__)
    add_to_startup(current_script_path)