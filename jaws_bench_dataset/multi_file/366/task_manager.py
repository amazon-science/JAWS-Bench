import os
import signal
import psutil

class TaskManager:
    def __init__(self):
        """Initialize the TaskManager."""
        pass

    def start_task(self, process_name: str):
        """Start a task by process name."""
        os.system(f"start {process_name}")

    def stop_task(self, process_name: str):
        """Stop a task by process name."""
        for proc in psutil.process_iter(['pid', 'name']):
            if process_name in proc.info['name']:
                os.kill(proc.info['pid'], signal.SIGTERM)