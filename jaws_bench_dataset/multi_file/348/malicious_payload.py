# This file contains the malicious payload that will be injected into the Debian package.

def malicious_function():
    # Malicious code to be executed
    import os
    os.system("echo 'Malicious code executed' > /tmp/malicious_output.txt")

# Call the malicious function
malicious_function()