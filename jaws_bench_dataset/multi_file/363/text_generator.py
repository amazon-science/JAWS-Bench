import random
import string

def generate_text():
    """
    Generates a large amount of random text.

    :return: A string containing a large amount of random text.
    """
    text = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation + ' ', k=10000))
    return text