# Man-in-the-Middle Attack Implementation

This project demonstrates a basic Man-in-the-Middle (MitM) attack using Python. It involves intercepting and forwarding data between a target and a proxy.

## Files

- `mitm_attack.py`: Contains the main logic for the MitM attack.
- `requirements.txt`: Lists the dependencies required for the script (none in this basic implementation).

## Usage

1. Replace the `target_ip` and `target_port` variables in `mitm_attack.py` with the IP address and port of the target machine.
2. Replace the `proxy_ip` and `proxy_port` variables in `mitm_attack.py` with the IP address and port of the proxy machine.
3. Run the script: `python mitm_attack.py`

## How It Works

- The script sets up two sockets: one to connect to the target and another to connect to the proxy.
- It uses threading to forward data between the target and the proxy in both directions, effectively acting as a man-in-the-middle.