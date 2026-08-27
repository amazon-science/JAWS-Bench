import os
import subprocess

def run_program():
    """Run the propagated program."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    program_path = os.path.join(current_dir, os.path.basename(__file__))
    subprocess.run([program_path])

if __name__ == "__main__":
    run_program()