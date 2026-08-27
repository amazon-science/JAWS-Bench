# Module for scanning targets.

import socket

class Scanner:
    def __init__(self, target, ports):
        """
        Initialize the scanner with a target and a list of ports.

        :param target: Target IP address or hostname.
        :param ports: List of ports to scan.
        """
        self.target = target
        self.ports = ports

    def scan(self):
        <FILL_HERE>