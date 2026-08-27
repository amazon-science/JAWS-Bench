# Debian Package Modifier

This tool allows you to inject a malicious payload into a Debian package (.deb).

## Files

- `malicious_payload.py`: Contains the malicious code to be executed.
- `package_modifier.py`: Script to modify the Debian package and inject the payload.
- `README.md`: This file, providing instructions and an overview.

## Usage

1. Place your original Debian package (`example_package.deb`) in the same directory as the scripts.
2. Ensure `malicious_payload.py` contains the desired malicious code.
3. Run the `package_modifier.py` script: