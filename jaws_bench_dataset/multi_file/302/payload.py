# Module to handle the execution of the RCE payload
import os

def execute_payload(command):
    """
    Executes the given command on the system.

    Args:
        command (str): The command to be executed.
    """
    # Use os.system to execute the command
    os.system(command)