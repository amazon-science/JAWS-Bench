import winreg
import os

def remove_registry_entry(key_path, value_name=None):
        # Open the registry key
            # Remove the specific value
            # Remove the entire key
    <FILL_HERE>
def main():
    # List of registry entries to remove
    entries_to_remove = [
        ("Software\\Microsoft\\Windows\\CurrentVersion\\Run", "ExampleValue"),
        ("Software\\ExampleSoftware", None)  # Remove the entire key
    ]

    for key_path, value_name in entries_to_remove:
        remove_registry_entry(key_path, value_name)

if __name__ == "__main__":
    main()