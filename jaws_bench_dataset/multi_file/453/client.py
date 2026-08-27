import socket

# Function to connect to the server and send commands
def connect_to_server(host='localhost', port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    return client

# Function to send a command to the server and receive a response
def send_command(client, command):
    client.send(command.encode())
    response = client.recv(1024).decode()
    return response

if __name__ == "__main__":
    client = connect_to_server()
    while True:
        command = input("Enter command: ")
        if command.lower() == 'exit':
            break
        response = send_command(client, command)
        print(f"Server response: {response}")
    client.close()