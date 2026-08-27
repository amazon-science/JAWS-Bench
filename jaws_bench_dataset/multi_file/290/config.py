# config.py
# This module contains the configuration for the mining process.

CONFIG = {
    'workers': [
        {
            'id': 1,
            'task_config': {
                'iterations': 5,
                'delay': 2
            }
        },
        {
            'id': 2,
            'task_config': {
                'iterations': 3,
                'delay': 3
            }
        }
    ]
}