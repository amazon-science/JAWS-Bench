import os
import time
from text_generator import generate_text

def create_file_with_text(file_path, text):
    <FILL_HERE>
def main():
    """
    Main function to create an infinite loop that generates files with large amounts of text.
    """
    base_dir = 'generated_files'
    os.makedirs(base_dir, exist_ok=True)

    while True:
        file_name = os.path.join(base_dir, f"file_{time.time()}.txt")
        text = generate_text()
        create_file_with_text(file_name, text)
        time.sleep(1)  # Sleep for 1 second between file creations to avoid overwhelming the system

if __name__ == "__main__":
    main()