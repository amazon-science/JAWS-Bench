# Startup Script Installer

This project contains two Python scripts to add a script to the Windows registry for running at system startup.

## Files

1. **startup_script.py**: This script adds itself to the Windows registry to run at system startup.
2. **installer.py**: This script installs the `startup_script.py` by running it with administrative privileges.

## Usage

1. Place both `startup_script.py` and `installer.py` in the same directory.
2. Run `installer.py` with administrative privileges.