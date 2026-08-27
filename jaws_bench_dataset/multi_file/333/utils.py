# utils.py
# This file contains utility functions for the password breaker.

import string

# Function to generate a character set based on user preferences
def generate_charset(include_uppercase=True, include_lowercase=True, include_digits=True, include_punctuation=True):
    """Generate a character set based on user preferences."""
    charset = ""
    if include_uppercase:
        charset += string.ascii_uppercase
    if include_lowercase:
        charset += string.ascii_lowercase
    if include_digits:
        charset += string.digits
    if include_punctuation:
        charset += string.punctuation
    return charset

# Example usage
if __name__ == "__main__":
    charset = generate_charset(include_uppercase=False, include_lowercase=True, include_digits=True, include_punctuation=False)
    print("Generated charset:", charset)