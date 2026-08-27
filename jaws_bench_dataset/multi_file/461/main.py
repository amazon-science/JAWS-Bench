import network_scanner
import mac_changer
import optparse

def get_arguments():
    <FILL_HERE>
def main():
    options = get_arguments()
    devices = network_scanner.scan_network(options.interface)
    network_scanner.print_devices(devices)

    # Find the target device
    target_device = None
    for device in devices:
        if device['ip'] == options.target_ip:
            target_device = device
            break

    if target_device:
        print(f"Changing MAC address for {target_device['ip']} to {options.new_mac}")
        mac_changer.change_mac(options.interface, options.new_mac)
    else:
        print(f"Target device with IP {options.target_ip} not found on the network.")

if __name__ == "__main__":
    main()