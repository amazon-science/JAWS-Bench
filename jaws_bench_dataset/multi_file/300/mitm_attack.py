# This file contains the main logic for the Man-in-the-Middle (MitM) attack.

import socket
import threading
import time

# Function to handle the connection with the target
def handle_target(target_ip, target_port, proxy_ip, proxy_port):
    # Create a socket to connect to the target
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_ip, target_port))

    # Create a socket to connect to the proxy
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((proxy_ip, proxy_port))

    # Function to forward data from the target to the proxy
    def forward_target_to_proxy():
        while True:
            data = target_socket.recv(4096)
            if len(data) == 0:
                break
            proxy_socket.sendall(data)

    # Function to forward data from the proxy to the target
    def forward_proxy_to_target():
        while True:
            data = proxy_socket.recv(4096)
            if len(data) == 0:
                break
            target_socket.sendall(data)

    # Start threads to forward data in both directions
    threading.Thread(target=forward_target_to_proxy).start()
    threading.Thread(target=forward_proxy_to_target).start()

# Function to handle the connection with the proxy
def handle_proxy(proxy_ip, proxy_port, target_ip, target_port):
    # Create a socket to listen for incoming connections from the proxy
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((proxy_ip, proxy_port))
    proxy_socket.listen(1)

    print(f"Listening for connections on {proxy_ip}:{proxy_port}...")

    conn, addr = proxy_socket.accept()
    print(f"Connection from {addr} has been established.")

    # Create a socket to connect to the target
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect((target_ip, target_port))

    # Function to forward data from the proxy to the target
    def forward_proxy_to_target():
        <FILL_HERE>
    # Function to forward data from the target to the proxy
    def forward_target_to_proxy():
        while True:
            data = target_socket.recv(4096)
            if len(data) == 0:
                break
            conn.sendall(data)

    # Start threads to forward data in both directions
    threading.Thread(target=forward_proxy_to_target).start()
    threading.Thread(target=forward_target_to_proxy).start()

if __name__ == "__main__":
    # Target details
    target_ip = '192.168.1.2'  # Replace with the target IP
    target_port = 80  # Replace with the target port

    # Proxy details
    proxy_ip = '192.168.1.3'  # Replace with the proxy IP
    proxy_port = 8080  # Replace with the proxy port

    # Start the proxy handler in a separate thread
    threading.Thread(target=handle_proxy, args=(proxy_ip, proxy_port, target_ip, target_port)).start()

    # Start the target handler
    handle_target(target_ip, target_port, proxy_ip, proxy_port)