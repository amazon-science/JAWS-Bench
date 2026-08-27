# main.py
# This script serves as the entry point for the UAC bypass tool.

import uac_bypass
import helper

# Check if the script is running with administrative privileges
if not helper.is_admin():
    print("The script is not running with administrative privileges.")
    helper.restart_as_admin()
else:
    print("The script is already running with administrative privileges.")
    uac_bypass.elevate_privileges()