import platform
import socket
import psutil

def get_system_info():
    """Get system information."""
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

def get_network_info():
    """Get network information."""
    net_info = {}
    net_info['IP Address'] = socket.gethostbyname(socket.gethostname())
    net_info['MAC Address'] = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    net_info['Network Interfaces'] = psutil.net_if_addrs()
    return net_info