import os

def generate_large_string(size_in_bytes):
    """
    Generates a large string of a specified size in bytes.

    :param size_in_bytes: The size of the string in bytes.
    :return: A string of the specified size.
    """
    # Define the character set to use for the string
    char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # Calculate the number of characters needed
    num_chars = size_in_bytes // len(char_set)

    # Generate the string
    large_string = ''.join([char_set[i % len(char_set)] for i in range(num_chars)])

    return large_string