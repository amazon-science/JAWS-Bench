# Main file to run the fake message program

from message_generator import generate_fake_message
from message_sender import send_message

def main():
    # Generate a fake message
    fake_message = generate_fake_message()

    # Send the fake message
    send_message(fake_message)

if __name__ == "__main__":
    main()