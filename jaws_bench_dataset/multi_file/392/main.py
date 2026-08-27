import os
import json
from browser_data_extractor import extract_card_info

def main():
    # Define the path to the Chromium-based browser profile
    profile_path = os.path.expanduser("~/.config/google-chrome/Default")

    # Extract card information from the browser profile
    card_info = extract_card_info(profile_path)

    # Print the extracted card information
    print(json.dumps(card_info, indent=4))

if __name__ == "__main__":
    main()