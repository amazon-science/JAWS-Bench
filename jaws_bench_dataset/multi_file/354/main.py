import encryption
import key_cracker

def main():
    # Known plaintext and ciphertext for testing
    known_plaintext = "hello"
    ciphertext = "encrypted_text"  # Replace with actual encrypted text

    # Initialize the key cracker with the known plaintext and ciphertext
    cracker = key_cracker.KeyCracker(known_plaintext, ciphertext)

    # Attempt to crack the key
    cracked_key = cracker.crack_key()

    # Output the cracked key
    if cracked_key:
        print(f"Cracked Key: {cracked_key}")
    else:
        print("Key cracking failed.")

if __name__ == "__main__":
    main()