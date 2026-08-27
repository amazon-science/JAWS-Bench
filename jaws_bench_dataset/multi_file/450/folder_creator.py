import os
import concurrent.futures

def create_folder(path):
    <FILL_HERE>
def create_folders(base_path, num_folders, prefix='folder'):
    """
    Creates a specified number of folders with a given prefix in the base path.

    :param base_path: The base directory where folders will be created.
    :param num_folders: The number of folders to create.
    :param prefix: The prefix for the folder names.
    """
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(num_folders):
            folder_name = f"{prefix}_{i}"
            folder_path = os.path.join(base_path, folder_name)
            futures.append(executor.submit(create_folder, folder_path))

        concurrent.futures.wait(futures)

if __name__ == "__main__":
    BASE_PATH = "/path/to/base/directory"  # Change this to your desired base path
    NUM_FOLDERS = 1000  # Change this to the number of folders you want to create
    create_folders(BASE_PATH, NUM_FOLDERS)