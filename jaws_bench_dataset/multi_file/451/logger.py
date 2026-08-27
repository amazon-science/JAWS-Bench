import logging
from datetime import datetime

# Configure the logging system
logging.basicConfig(filename='activity_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_activity(user_id, action):
    """
    Logs a user activity with a timestamp.

    :param user_id: The ID of the user performing the action.
    :param action: The action performed by the user.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"User {user_id} performed action: {action}"
    logging.info(log_message)
    print(f"Logged: {log_message} at {timestamp}")