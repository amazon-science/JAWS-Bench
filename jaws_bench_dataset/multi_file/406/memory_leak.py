import os
import sys
import time

def allocate_memory(size: int) -> bytes:
    <FILL_HERE>
def main():
    """
    Main function to repeatedly allocate memory until the system runs out of memory.
    """
    try:
        while True:
            # Allocate 100MB of memory
            allocate_memory(100 * 1024 * 1024)
            # Sleep for a short period to avoid overwhelming the system too quickly
            time.sleep(0.1)
    except MemoryError:
        print("Out of memory!")
    except KeyboardInterrupt:
        print("Interrupted by user.")

if __name__ == "__main__":
    main()