import time
import threading
from http_client import HttpClient

def main(target_ip, interval):
    """
    Main function to start the infinite loop for HTTP connection attempts.

    :param target_ip: The target IP address to connect to.
    :param interval: The time interval between connection attempts in seconds.
    """
    while True:
        # Create an instance of HttpClient
        client = HttpClient(target_ip)
        # Start a new thread to handle the HTTP connection
        thread = threading.Thread(target=client.connect_and_request)
        thread.start()
        # Wait for the specified interval before the next attempt
        time.sleep(interval)

if __Name__ == "__main__":
    # Example usage
    TARGET_IP = "192.168.1.1"  # Replace with the target IP address
    INTERVAL = 5  # Time interval between connection attempts in seconds
    main(TARGET_IP, INTERVAL)