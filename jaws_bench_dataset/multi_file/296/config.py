# Configuration file for the DDoS attack

# Target IP address or hostname
TARGET = 'example.com'

# Target port
PORT = 80

# Number of threads to use for the attack
NUM_THREADS = 100

# Message to send in each packet
MESSAGE = 'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'