import ctypes
from graphics import GraphicsManipulator

def main():
    # Create an instance of GraphicsManipulator
    gm = GraphicsManipulator()

    # Example usage: Change screen resolution
    gm.change_resolution(1024, 768)

    # Example usage: Change screen brightness
    gm.change_brightness(50)

    # Example usage: Capture screenshot
    gm.capture_screenshot('screenshot.png')

if __name__ == "__main__":
    main()