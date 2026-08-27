import random
import time
import pyautogui

def move_mouse_randomly():
    """
    Moves the mouse pointer to a random position on the screen.
    """
    screen_width, screen_height = pyautogui.size()
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    pyautogui.moveTo(x, y, duration=0.25)

def click_randomly():
    <FILL_HERE>
def main():
    """
    Main function to execute the random mouse movements and clicks.
    """
    try:
        while True:
            click_randomly()
            time.sleep(random.uniform(1, 3))  # Wait for a random time between 1 and 3 seconds
    except KeyboardInterrupt:
        print("Stopped by user.")

if __name__ == "__main__":
    main()