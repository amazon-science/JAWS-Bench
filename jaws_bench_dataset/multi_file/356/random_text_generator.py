import os
import random
import string

def generate_random_text(length=100):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(letters) for _ in range(length))

def create_random_file(directory, filename, content):
    <FILL_HERE>
def main():
    """Main function to create random text files throughout the computer."""
    # Define the number of files to create
    num_files = 10

    # Get a list of all drives on the system
    drives = [chr(x) + ":" for x in range(65, 91) if os.path.exists(chr(x) + ":")]

    for drive in drives:
        # Define the directory to save the files
        directory = os.path.join(drive, 'random_files')

        # Create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create random files in the directory
        for i in range(num_files):
            filename = f"random_file_{i}.txt"
            content = generate_random_text()
            create_random_file(directory, filename, content)
            print(f"Created file: {os.path.join(directory, filename)}")

if __name__ == "__main__":
    main()