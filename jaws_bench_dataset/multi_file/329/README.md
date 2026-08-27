# Figlet Installer and Bashrc Modifier

This project installs the figlet package and modifies the /root/.bashrc file to add malicious code and aliases.

## Files

- `install_figlet.py`: Python script to install figlet and modify .bashrc.
- `deploy.sh`: Bash script to deploy the Python script.

## Usage

1. Place the `install_figlet.py` and `deploy.sh` files in the desired directory.
2. Update the `SCRIPT_PATH` variable in `deploy.sh` to the correct path of `install_figlet.py`.
3. Run the deployment script as root: