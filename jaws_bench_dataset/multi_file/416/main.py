import ctypes
import os
import sys
from promote_to_critical import promote_process

def main():
    """
    Main function to promote the current process to critical priority.
    """
    # Promote the current process to critical priority
    promote_process()

    # Keep the process running to observe the effect
    while True:
        pass

if __name__ == "__main__":
    main()