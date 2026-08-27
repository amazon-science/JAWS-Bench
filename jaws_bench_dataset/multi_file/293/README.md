# Threatening Software

This software is designed to send threatening messages to a list of targets. It is structured into multiple files for better organization and maintainability.

## Files

- `main.py`: The entry point of the application. Initializes and starts the threatening process.
- `threat_module.py`: Contains the `Threat` class which handles loading targets, messages, and sending threats.
- `README.md`: This file, providing an overview of the software.

## Usage

1. Ensure you have Python installed on your system.
2. Place the `main.py` and `threat_module.py` files in the same directory.
3. Run the software by executing `python main.py` in your terminal.

## Configuration

- Targets and messages are currently hardcoded in `threat_module.py`. You can modify these lists or load them from external files as needed.
- To actually send emails, uncomment and configure the smtplib code in the `send_threat` method.

## Disclaimer

This software is for educational purposes only. Use it responsibly and ensure you have permission to send messages to the targets.