# This module contains the payload to be executed by the trojan horse.
# The payload can be any malicious code or action.

def execute_payload():
    """
    Function to execute the payload.
    This is where the malicious action takes place.
    """
    # Example payload: Create a hidden file in the user's home directory
    import os

    home_dir = os.path.expanduser("~")
    hidden_file_path = os.path.join(home_dir, ".hidden_trojan_file")

    with open(hidden_file_path, 'w') as f:
        f.write("This is a hidden file created by the trojan horse.")

    print(f"Payload executed: Hidden file created at {hidden_file_path}")