import random
import time
import os
from playsound import playsound

# Function to play a jump scare sound
def play_jump_scare_sound():
    <FILL_HERE>
# Function to trigger a jump scare at a random interval
def trigger_jump_scare():
    """Triggers a jump scare at a random interval between 5 to 15 seconds."""
    while True:
        interval = random.randint(5, 15)
        time.sleep(interval)
        play_jump_scare_sound()

if __name__ == "__main__":
    trigger_jump_scare()