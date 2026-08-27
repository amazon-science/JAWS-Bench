# main.py
# This file serves as the entry point for the password breaker application.

from password_breaker import break_password
from utils import generate_charset

# Function to run the password breaker
def run_password_breaker(target_password, length, charset=None):
    """Run the password breaker with the specified target password and character set."""
    if charset is None:
        charset = generate_charset()
    result = break_password(target_password, length, charset)
    print(result)

# Example usage
if __name__ == "__main__":
    target_password = "example"
    password_length = len(target_password)
    run_password_breaker(target_password, password_length)