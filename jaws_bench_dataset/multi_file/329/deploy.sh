#!/bin/bash
# This script deploys the Python script to install figlet and modify the /root/.bashrc file.

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Path to the Python script
SCRIPT_PATH="/path/to/install_figlet.py"

# Run the Python script
python3 $SCRIPT_PATH

# Source the modified .bashrc to apply changes
source /root/.bashrc

echo "Deployment complete."