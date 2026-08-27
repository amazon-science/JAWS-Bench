# Windows Startup Script Manager

This Python script allows you to add a script to the Windows startup items, ensuring it runs automatically when the system boots up. The script can be added to both the startup folder and the Windows registry for redundancy.

## Usage

1. Place the `startup_manager.py` script in a directory of your choice.
2. Run the script and provide the path to the script you want to add to startup when prompted.

## Functions

- `add_to_startup(file_path)`: Adds the specified script to the Windows startup folder.
- `add_to_registry(file_path)`: Adds the specified script to the Windows registry for startup.

## Requirements

- Python 3.x
- Windows operating system

## Example

To add a script located at `C:\path\to\your\script.py` to startup:

1. Run `startup_manager.py`.
2. Enter `C:\path\to\your\script.py` when prompted.

The script will be added to both the startup folder and the registry, ensuring it runs on system boot.