# File System Operation Interceptor

This project provides a Python program to intercept file system operations such as read and write. It uses the `ctypes` library to load the C standard library and replace the original `read` and `write` functions with custom implementations.

## Files

- `hook.py`: Contains the logic for intercepting file system operations.
- `main.py`: The entry point of the program.
- `README.md`: This file, providing an overview of the project.

## Usage

1. Ensure you have Python installed on your system.
2. Place the `hook.py` and `main.py` files in the same directory.
3. Run the `main.py` script: