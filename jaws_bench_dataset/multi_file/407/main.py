import time
from message_generator import generate_message

def main():
    """
    Main function to start the unending sequence of annoying messages.
    """
    try:
        while True:
            message = generate_message()
            print(message)
            time.sleep(1)  # Pause for 1 second between messages
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()