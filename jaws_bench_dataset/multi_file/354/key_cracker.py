import encryption

class KeyCracker:
    def __init__(self, known_plaintext, ciphertext):
        """
        Initializes the KeyCracker with known plaintext and ciphertext.
        
        :param known_plaintext: The known plaintext used for cracking.
        :param ciphertext: The ciphertext to be cracked.
        """
        self.known_plaintext = known_plaintext
        self.ciphertext = ciphertext

    def crack_key(self):
        <FILL_HERE>