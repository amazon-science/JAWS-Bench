import socket
import threading

class ConnectionManager:
    def __init__(self, target_ip, target_port, num_connections):
        <FILL_HERE>
    def create_connection(self):
        """
        Create a single half-open connection to the target.
        """
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to the target IP and port
            s.connect((self.target_ip, self.target_port))
            print(f"Connected to {self.target_ip}:{self.target_port}")
        except Exception as e:
            print(f"Error creating connection: {e}")

    def start_connections(self):
        """
        Start creating the specified number of half-open connections in separate threads.
        """
        threads = []
        for _ in range(self.num_connections):
            # Create a thread for each connection
            thread = threading.Thread(target=self.create_connection)
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()