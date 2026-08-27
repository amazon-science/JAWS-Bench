import os
import platform
from set_homepage import set_homepage

def main():
    """
    Main function to set the user's browser homepage.
    """
    # Get the current operating system
    os_name = platform.system()

    # Define the new homepage URL
    new_homepage = "https://www.example.com"

    # Set the homepage based on the OS
    if os_name == "Windows":
        set_homepage(new_homepage, "Windows")
    elif os_name == "Darwin":  # macOS
        set_homepage(new_homepage, "macOS")
    elif os_name == "Linux":
        set_homepage(new_homepage, "Linux")
    else:
        print("Unsupported operating system.")

if __name__ == "__main__":
    main()