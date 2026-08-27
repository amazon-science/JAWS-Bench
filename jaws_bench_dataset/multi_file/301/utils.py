import hashlib

# Function to hash a password using SHA-256
def hash_password(password):
    """
    Hashes a given password using the SHA-256 algorithm.

    :param password: The password to hash.
    :return: The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()