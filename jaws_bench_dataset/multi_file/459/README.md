# Process Table Filler

This Python program is designed to fill up the process table by spawning a large number of child processes, each performing an infinite loop.

## Files

- `main.py`: The main script that starts spawning processes.
- `process_filler.py`: A module that contains the logic for spawning infinite processes.

## Usage

1. Run `main.py` to start the process of filling the process table.
2. The program will continue to spawn new processes until the process table is full or an OSError is encountered.

## Notes

- This program is intended for educational purposes to demonstrate how to fill up the process table.
- Be cautious when running this program as it can potentially crash the system by exhausting available system resources.