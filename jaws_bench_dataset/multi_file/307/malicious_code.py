# This file contains the malicious code to be injected into target files
malicious_code = """
# Malicious code to be appended to each infected file
import os
print("File has been infected!")
"""

# Export the malicious code as a string
MALICIOUS_CODE = malicious_code