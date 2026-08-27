import os
import sys
import time

def child_task():
    """
    Function to simulate a task performed by the child process.
    """
    print(f"Child process {os.getpid()} is performing a task.")
    # Simulate some work
    time.sleep(5)
    print(f"Child process {os.getpid()} has completed its task.")

if __name__ == "__main__":
    child_task()
    sys.exit(0)