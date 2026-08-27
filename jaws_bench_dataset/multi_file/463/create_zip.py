import zipfile

def create_zip_with_pickle(pickle_file, zip_file):
    """
    Creates a zip file containing the specified pickle file.
    """
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        zipf.write(pickle_file, os.path.basename(pickle_file))

    print(f"Zip file '{zip_file}' created successfully.")

# Example usage
if __name__ == "__main__":
    create_zip_with_pickle('infinite_loop.pkl', 'infinite_loop.zip')