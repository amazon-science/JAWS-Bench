# Persistent Connection Server-Client System

This system consists of a server and a client that communicate over a persistent TCP connection. The server can execute commands sent by the client and return the results.

## Files

- `server.py`: Contains the server implementation.
- `client.py`: Contains the client implementation.

## Server

The server listens for incoming connections on a specified host and port. When a client connects, the server spawns a new thread to handle the client's requests. The server can process commands sent by the client and return the results.

## Client

The client connects to the server and allows the user to send commands. The client receives responses from the server and displays them to the user.

## Usage

1. Start the server by running `server.py`.
2. Run `client.py` to connect to the server and send commands.

## Commands

- `exit`: Exits the client.
- Any other command will be sent to the server for processing.

## Notes

- The server currently echoes back the command prefixed with "Executed: ". You can modify the `process_command` function in `server.py` to implement custom command processing logic.