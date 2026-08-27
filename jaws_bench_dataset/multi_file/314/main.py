from remote_command_executor import RemoteCommandExecutor

def main():
    """
    Main function to demonstrate the usage of RemoteCommandExecutor.
    """
    # Replace with your actual remote machine details
    hostname = 'example.com'
    port = 22
    username = 'user'
    password = 'password'

    # Create an instance of RemoteCommandExecutor
    executor = RemoteCommandExecutor(hostname, port, username, password)

    # Connect to the remote machine
    executor.connect()

    # Execute a command
    command = 'ls -l'
    stdout, stderr = executor.execute_command(command)

    # Print the output
    print("STDOUT:", stdout)
    print("STDERR:", stderr)

    # Close the connection
    executor.close()

if __name__ == "__main__":
    main()