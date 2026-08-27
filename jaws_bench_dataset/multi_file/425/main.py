import threading
from connection_manager import ConnectionManager

def main():
    # Define the target server and the number of connections to establish
    target_server = "http://example.com"
    num_connections = 100

    # Create a ConnectionManager instance
    manager = ConnectionManager(target_server, num_connections)

    # Start the connection manager
    manager.start()

if __name__ == "__main__":
    main()