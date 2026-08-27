# scanner.py - Module for scanning the network for vulnerable hosts

import socket

def scan_network():
    # Scan the local network for vulnerable hosts
    # Return a list of IP addresses of vulnerable hosts
    vulnerable_hosts = []
    for ip in range(1, 255):
        try:
            # Check if the host is up and vulnerable
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('192.168.1.' + str(ip), 22))
            if result == 0:
                vulnerable_hosts.append('192.168.1.' + str(ip))
            sock.close()
        except Exception as e:
            print(f"Error scanning {ip}: {e}")
    return vulnerable_hosts