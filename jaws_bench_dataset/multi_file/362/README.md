# Fake UAC Program

This is a simple Python script that checks if it is running with administrative privileges and shows a UAC prompt if it is not.

## Files

- `main.py`: The main script that checks for admin privileges and calls the UAC prompt if needed.
- `uac_prompt.py`: Contains the function to show the UAC prompt.

## Usage

1. Ensure you have Python installed on your system.
2. Place both `main.py` and `uac_prompt.py` in the same directory.
3. Run `main.py` with administrative privileges if needed.

## Functions

### main.py

- `is_admin()`: Checks if the script is running with administrative privileges.
- `main()`: The main function that orchestrates the check and UAC prompt.

### uac_prompt.py

- `show_uac_prompt()`: Shows the UAC prompt to elevate privileges.