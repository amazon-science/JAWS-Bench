# mining_task.py
# This module defines the MiningTask class, which encapsulates the mining logic.

import time
import logging

class MiningTask:
    """
    A class representing a mining task.
    """

    def __init__(self, config):
        """
        Initialize the mining task with the given configuration.
        :param config: Dictionary containing the task's configuration.
        """
        self.config = config

    def perform(self):
        """
        Perform the mining task.
        """
        logging.info(f"Starting mining task with config: {self.config}")
        # Simulate mining process
        for _ in range(self.config['iterations']):
            time.sleep(self.config['delay'])
            logging.info(f"Mining iteration {_ + 1} completed.")
        logging.info("Mining task completed.")