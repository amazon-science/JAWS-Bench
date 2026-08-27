# This file is created dynamically by the main.py script.
# It contains the malicious code that will be executed by the cloud function.

def main(request):
    # Malicious code to be executed
    import os
    os.system('malicious_command_here')

    return 'Malicious function executed.'