# deploy.py
# This file handles the deployment of the obfuscated code.

import os
import obfuscator

def deploy_obfuscated_code(output_file, code):
    """Deploy the obfuscated code to a specified output file."""
    with open(output_file, 'w') as file:
        file.write(code)

if __name__ == "__main__":
    # Example usage
    malicious_code = """
print("Malicious code executed!")
# Add your malicious code here
    """
    obfuscated_code = obfuscator.obfuscate_code(malicious_code)
    deploy_obfuscated_code('malicious_script.py', obfuscated_code)