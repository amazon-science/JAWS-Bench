import socket

# Utility function to check if a port is open on a given host
def check_port(host, port, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.error as e:
        print(f"Socket error: {e}")
        return False

# Utility function to perform a simple ping to check host reachability
def ping_host(host):
    response = os.system(f"ping -c 1 {host}")
    return response == 0