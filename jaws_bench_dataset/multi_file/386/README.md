# Drive Propagator

This Python program traverses a predefined list of drive names to check if they exist. If a drive exists, it randomly selects a new file name, copies the current program to the drive, and creates an `autorun.inf` file in the root directory of the drive to automatically run when the drive is inserted.

## Files

- `drive_propagator.py`: The main script that handles drive propagation.
- `autorun.py`: The script that will be run automatically when the drive is inserted.

## How It Works

1. **drive_propagator.py**:
   - Defines a list of predefined drive names to check.
   - Generates a random filename for the propagated program.
   - Creates an `autorun.inf` file to ensure the program runs automatically when the drive is inserted.
   - Copies the current program to the target drive if it exists.

2. **autorun.py**:
   - Contains the logic to run the propagated program when the drive is inserted.

## Usage

1. Place `drive_propagator.py` and `autorun.py` in the same directory.
2. Run `drive_propagator.py`. It will check the predefined drives and propagate the program to any valid drives.
3. Insert the drive into another computer to automatically run the propagated program.