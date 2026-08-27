import subprocess
import optparse

def get_arguments():
    """
    Parses command-line arguments for the MAC changer.
    
    :return: Parsed arguments.
    """
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    """
    Changes the MAC address of the specified interface.
    
    :param interface: The network interface to change.
    :param new_mac: The new MAC address to set.
    """
    print("[+] Changing MAC address for " + interface + " to " + new_mac)

    # Turn down the interface
    subprocess.call(["ifconfig", interface, "down"])
    # Change the MAC address
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    # Turn up the interface
    subprocess.call(["ifconfig", interface, "up"])

if __name__ == "__main__":
    options = get_arguments()
    change_mac(options.interface, options.new_mac)