# Backdoor Implementation

This backdoor implementation consists of two main files: `backdoor.py` and `installer.py`.

## Files

1. **backdoor.py**: This is the main backdoor script that listens for incoming connections and executes commands received from the attacker.

2. **installer.py**: This script installs the backdoor by copying `backdoor.py` to a hidden location and starting it in the background.

## Usage

1. Place both `backdoor.py` and `installer.py` in the same directory.
2. Run `installer.py` to install and start the backdoor: