import threading
import block_input

def start_blocking():
    """
    Starts the input blocking in a separate thread.
    """
    blocking_thread = threading.Thread(target=block_input.block_input)
    blocking_thread.start()

if __name__ == "__main__":
    start_blocking()