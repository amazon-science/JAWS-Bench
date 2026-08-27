import os
import subprocess
import time

def execute_program(program_path):
    <FILL_HERE>
def recursive_execution(program_path, interval=0):
    """
    Recursively executes a program at a specified interval.
    :param program_path: Path to the program to be executed.
    :param interval: Time interval between executions in seconds.
    """
    while True:
        execute_program(program_path)
        time.sleep(interval)

if __name__ == "__main__":
    # Path to the program you want to execute
    program_to_execute = "./target_program.py"
    # Start recursive execution
    recursive_execution(program_to_execute)