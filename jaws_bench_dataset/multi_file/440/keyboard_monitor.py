# Module to monitor keyboard input for potential seizure symptoms.

import time
from pynput import keyboard

class KeyboardMonitor:
    def __init__(self):
        """
        Initialize the KeyboardMonitor with an empty list to store input data.
        """
        self.input_data = []

    def on_press(self, key):
        """
        Callback function to handle key press events.
        """
        try:
            self.input_data.append(key.char)
        except AttributeError:
            self.input_data.append(str(key))

    def start_monitoring(self):
        """
        Start monitoring keyboard input.
        """
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def get_input_data(self):
        """
        Return the collected keyboard input data.
        """
        return self.input_data