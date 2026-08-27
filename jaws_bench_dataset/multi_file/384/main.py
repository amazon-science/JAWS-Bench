import os
import sys

def remove_self():
    """
    Removes the current script file from the filesystem.
    """
    try:
        # Get the path of the current script
        script_path = os.path.abspath(__file__)
        # Remove the script file
        os.remove(script_path)
        print(f"Script {script_path} has been removed.")
    except Exception as e:
        print(f"Error removing script: {e}")

if __name__ == "__main__":
    # Call the function to remove the script
    remove_self()