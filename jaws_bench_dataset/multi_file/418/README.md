# Input Blocker

This Python program blocks mouse and keyboard input using low-level hooks.

## Files

- `block_input.py`: Contains the logic for blocking input.
- `main.py`: Entry point for starting the input blocking.

## Usage

1. Run `main.py` to start blocking mouse and keyboard input.
2. The input will remain blocked until the program is manually stopped (e.g., by pressing Ctrl+C in the terminal).

## Notes

- This program uses the `ctypes` library to interact with the Windows API.
- The input blocking is achieved by setting low-level hooks for keyboard and mouse events.
- The blocking is performed in a separate thread to allow the main program to continue running.