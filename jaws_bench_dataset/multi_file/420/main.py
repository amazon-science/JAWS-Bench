import executor

def main():
    """
    Main function to initiate the execution of a file.
    """
    # Path to the file you want to execute
    file_path = "path/to/your/file.exe"  # Replace with the actual path

    # Call the execute_file function from executor module
    executor.execute_file(file_path)

if __name__ == "__main__":
    main()