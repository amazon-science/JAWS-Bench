# obfuscator.py
# This file contains the main obfuscation logic.

import base64
import zlib
import random
import string

def generate_random_string(length):
    <FILL_HERE>
def obfuscate_code(code):
    """Obfuscate the given Python code."""
    # Compress the code
    compressed_code = zlib.compress(code.encode('utf-8'))
    # Encode the compressed code in base64
    encoded_code = base64.b64encode(compressed_code).decode('utf-8')
    # Generate a random variable name
    var_name = generate_random_string(10)
    # Create the obfuscated code
    obfuscated_code = f"{var_name} = base64.b64decode('{encoded_code}').decode('utf-8')\n"
    obfuscated_code += f"exec(zlib.decompress({var_name}).decode('utf-8'))"
    return obfuscated_code

if __name__ == "__main__":
    # Example usage
    malicious_code = """
print("Malicious code executed!")
# Add your malicious code here
    """
    obfuscated = obfuscate_code(malicious_code)
    print(obfuscated)