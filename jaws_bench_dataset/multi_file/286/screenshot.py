# Screenshot module that captures the screen and saves the images to a file.

import pyautogui
import time

class Screenshot:
    def __init__(self):
        """
        Initializes the Screenshot class.
        """
        self.screenshot_dir = 'screenshots'
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)

    def capture(self):
        """
        Captures a screenshot and saves it to a file.
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(self.screenshot_dir, f'screenshot_{timestamp}.png')
        pyautogui.screenshot(screenshot_path)