import hook

# Main function to start the interception
def main():
    # Call the function to intercept file system operations
    hook.intercept_file_operations()

if __name__ == "__main__":
    main()