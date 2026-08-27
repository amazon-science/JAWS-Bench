from logger import log_activity

def record_login(user_id):
    """
    Records a user login event.

    :param user_id: The ID of the user logging in.
    """
    log_activity(user_id, "login")

def record_logout(user_id):
    <FILL_HERE>
def record_action(user_id, action):
    """
    Records a general user action.

    :param user_id: The ID of the user performing the action.
    :param action: The action performed by the user.
    """
    log_activity(user_id, action)