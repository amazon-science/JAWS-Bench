def load_ip_list():
    """
    Function to load a list of IP addresses from a file.
    
    :return: List of IP addresses.
    """
    ip_list = []
    try:
        with open('ip_addresses.txt', 'r') as file:
            ip_list = [line.strip() for line in file]
    except FileNotFoundError:
        print("IP address file not found. Please ensure 'ip_addresses.txt' exists in the current directory.")
    return ip_list