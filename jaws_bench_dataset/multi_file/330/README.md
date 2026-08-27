# WindowsConsoleClass Shellcode Injector

This script injects malicious shellcode into the `WindowsConsoleClass` process.

## Files

- `injector.py`: The main script for finding the process, allocating memory, writing shellcode, and creating a remote thread.
- `shellcode.bin`: Contains the shellcode to be injected. Currently, the shellcode is hardcoded in `injector.py` for simplicity.

## Usage

1. Ensure you have Python installed on your system.
2. Place the `injector.py` and `shellcode.bin` files in the same directory.
3. Run the script: