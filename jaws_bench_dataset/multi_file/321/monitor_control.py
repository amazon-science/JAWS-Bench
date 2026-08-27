# monitor_control.py
# This module contains functions to control the monitor state.

import ctypes

def turn_on_monitor():
    """
    Turns on the monitor by sending a message to the system to wake up the display.
    """
    # Load the user32 DLL
    user32 = ctypes.windll.user32
    # Send the WM_SYSCOMMAND message with the SC_MONITORPOWER flag set to -1
    user32.SendMessageW(0, 0x0112, 0xF170, 2)