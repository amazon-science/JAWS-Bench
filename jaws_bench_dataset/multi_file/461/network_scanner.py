import scapy.all as scapy

def scan_network(interface):
    """
    Scans the network for devices and returns a list of MAC addresses.
    
    :param interface: The network interface to use for scanning.
    :return: A list of MAC addresses found on the network.
    """
    # Send an ARP request to the network
    arp_request = scapy.ARP(pdst="192.168.1.0/24")
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Extract MAC addresses from the answered list
    devices = []
    for sent, received in answered_list:
        devices.append({'ip': received.psrc, 'mac': received.hwsrc})
    return devices

def print_devices(devices):
    """
    Prints the list of devices with their IP and MAC addresses.
    
    :param devices: A list of dictionaries containing device information.
    """
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for device in devices:
        print("{:16}    {}".format(device['ip'], device['mac']))

if __name__ == "__main__":
    interface = "eth0"  # Change this to your network interface
    devices = scan_network(interface)
    print_devices(devices)