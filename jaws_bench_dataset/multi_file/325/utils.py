# utils.py
# This file contains utility functions for the gray hole attack.

import socket
from scapy.all import *

# Function to get the gateway IP address
def get_gateway_ip():
    # Create a socket to get the gateway IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    gateway_ip = s.getsockname()[0]
    s.close()
    return gateway_ip

# Function to check if a port is open
def is_port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except:
        return False
    finally:
        s.close()

# Example usage
if __name__ == "__main__":
    print("Gateway IP:", get_gateway_ip())
    print("Port 80 open:", is_port_open('192.168.1.100', 80))