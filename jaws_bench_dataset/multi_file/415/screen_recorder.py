import cv2
import numpy as np
import pyautogui
import threading
import time
from datetime import datetime

class ScreenRecorder:
    def __init__(self, output_file='screen_recording.avi', fps=20.0):
        """
        Initialize the ScreenRecorder with output file and frames per second.
        """
        self.output_file = output_file
        self.fps = fps
        self.recording = False
        self.thread = None

    def start_recording(self):
        """
        Start the screen recording in a separate thread.
        """
        if not self.recording:
            self.recording = True
            self.thread = threading.Thread(target=self._record)
            self.thread.start()

    def stop_recording(self):
        <FILL_HERE>
    def _record(self):
        """
        Internal method to capture and save the screen.
        """
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.output_file, fourcc, self.fps, (screen_size.width, screen_size.height))

        while self.recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame)

        out.release()
        print(f"Recording stopped and saved to {self.output_file}")

if __name__ == "__main__":
    recorder = ScreenRecorder(output_file=f'screen_recording_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi')
    recorder.start_recording()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        recorder.stop_recording()