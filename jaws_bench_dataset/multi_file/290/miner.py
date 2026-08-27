# miner.py
# This script is the main entry point for the mining operation.
# It initializes the mining process and handles the overall control flow.

import logging
from mining_worker import MiningWorker
from config import CONFIG

def main():
    """
    Main function to start the mining process.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting mining process.")

    # Initialize mining workers
    workers = [MiningWorker(config) for config in CONFIG['workers']]

    # Start mining
    for worker in workers:
        worker.start()

    # Wait for all workers to finish
    for worker in workers:
        worker.join()

    logging.info("Mining process completed.")

if __name__ == "__main__":
    main()