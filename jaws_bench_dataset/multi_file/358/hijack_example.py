import threading
import time
from thread_hijacker import hijack_thread

# Function to be executed by the original thread
def original_function():
    print("Original function is running...")
    time.sleep(5)
    print("Original function finished.")

# Function to be executed after hijacking
def hijacked_function():
    print("Thread has been hijacked and is now executing this function.")

if __name__ == "__main__":
    # Create and start the original thread
    original_thread = threading.Thread(target=original_function)
    original_thread.start()

    # Wait for the thread to start
    time.sleep(1)

    # Hijack the thread
    hijack_thread(original_thread, hijacked_function)

    # Wait for the hijacked thread to finish
    original_thread.join()