import subprocess
import time

def start_uac_prompts():
    """Start the UAC prompt process."""
    while True:
        # Start the uac_prompt.py script in a new process
        subprocess.Popen(["python", "uac_prompt.py"])
        time.sleep(1)  # Add a delay to avoid rapid successive prompts

if __name__ == "__main__":
    start_uac_prompts()