import threading
import time
import random
import pygetwindow as gw
import math

# Function to generate random coordinates using cosine and sine functions
def generate_random_coordinates():
    <FILL_HERE>
# Function to move the window to random coordinates
def move_window(window, x, y):
    window.moveTo(x, y)

# Function to monitor window changes and move the activated window
def monitor_windows():
    previous_active_window = None
    while True:
        active_window = gw.getActiveWindow()
        if active_window != previous_active_window:
            previous_active_window = active_window
            if active_window:
                x, y = generate_random_coordinates()
                threading.Thread(target=move_window, args=(active_window, x, y)).start()
        time.sleep(1)  # Adjust the sleep interval as needed

if __name__ == "__main__":
    threading.Thread(target=monitor_windows).start()