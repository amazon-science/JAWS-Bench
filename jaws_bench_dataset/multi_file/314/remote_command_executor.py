import paramiko
import sys

class RemoteCommandExecutor:
    def __init__(self, hostname, port, username, password):
        """
        Initializes the RemoteCommandExecutor with the given connection details.

        :param hostname: The hostname or IP address of the remote machine.
        :param port: The port number to connect to (default is 22 for SSH).
        :param username: The username to use for authentication.
        :param password: The password to use for authentication.
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        """
        Establishes a connection to the remote machine.
        """
        try:
            self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            print("Connected to", self.hostname)
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            sys.exit(1)
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
            sys.exit(1)
        except Exception as e:
            print(f"Exception in connecting: {e}")
            sys.exit(1)

    def execute_command(self, command):
        """
        Executes a command on the remote machine.

        :param command: The command to be executed.
        :return: The output of the command.
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        <FILL_HERE>
# Example usage:
# if __name__ == "__main__":
#     executor = RemoteCommandExecutor('example.com', 22, 'user', 'password')
#     executor.connect()
#     stdout, stderr = executor.execute_command('ls -l')
#     print("STDOUT:", stdout)
#     print("STDERR:", stderr)
#     executor.close()