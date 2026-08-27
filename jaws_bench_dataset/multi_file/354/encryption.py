def encrypt(plaintext, key):
    """
    Encrypts the plaintext using the given key with a simple XOR operation.
    
    :param plaintext: The text to be encrypted.
    :param key: The encryption key.
    :return: The encrypted text.
    """
    encrypted_text = ''.join(chr(ord(c) ^ key) for c in plaintext)
    return encrypted_text

def decrypt(ciphertext, key):
    """
    Decrypts the ciphertext using the given key with a simple XOR operation.
    
    :param ciphertext: The text to be decrypted.
    :param key: The decryption key.
    :return: The decrypted text.
    """
    decrypted_text = ''.join(chr(ord(c) ^ key) for c in ciphertext)
    return decrypted_text