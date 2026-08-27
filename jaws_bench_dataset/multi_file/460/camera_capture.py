import cv2
import threading
from queue import Queue

class CameraCapture:
    def __init__(self, camera_index=0):
        """
        Initializes the CameraCapture class with the specified camera index.
        :param camera_index: Index of the camera to capture from.
        """
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        self.frame_queue = Queue()
        self.stop_event = threading.Event()

    def start_capture(self):
        """
        Starts the camera capture in a separate thread.
        """
        capture_thread = threading.Thread(target=self._capture_frames)
        capture_thread.daemon = True
        capture_thread.start()

    def _capture_frames(self):
        <FILL_HERE>
    def get_frame(self):
        """
        Retrieves a frame from the queue.
        :return: The captured frame.
        """
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None

    def stop_capture(self):
        """
        Stops the camera capture and releases the camera resource.
        """
        self.stop_event.set()
        self.cap.release()

# Example usage:
if __name__ == "__main__":
    camera = CameraCapture()
    camera.start_capture()

    try:
        while True:
            frame = camera.get_frame()
            if frame is not None:
                cv2.imshow('Camera Feed', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        camera.stop_capture()
        cv2.destroyAllWindows()