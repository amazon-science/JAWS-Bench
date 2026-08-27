# Module to send messages

def send_message(message):
    """
    Simulates sending a message.

    Args:
        message (dict): A dictionary containing 'sender' and 'content' of the message.
    """
    sender = message["sender"]
    content = message["content"]
    print(f"Sending message from {sender}: {content}")