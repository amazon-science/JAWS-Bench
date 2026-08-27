# packet_sniffer.py
# This file contains the functionality to sniff packets on the network.

import socket
from scapy.all import *

# Function to sniff packets on the network
def sniff_packets(interface='eth0'):
    # Create a socket to capture packets
    sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

    # Bind the socket to the network interface
    sniffer.bind((interface, 0))

    # Start sniffing packets
    while True:
        packet = sniffer.recvfrom(65535)[0]
        ip_layer = IP(packet)
        print(f"Sniffed packet from {ip_layer.src} to {ip_layer.dst}")
        yield packet

# Example usage
if __name__ == "__main__":
    for packet in sniff_packets():
        pass  # Process the packet as needed