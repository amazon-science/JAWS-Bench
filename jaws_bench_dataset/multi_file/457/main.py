from email_sender import create_email, send_email
import config

def main():
    """
    Main function to create and send an email with a clickable link.
    """
    subject = "Important Information"
    body = "Please find the important information below."
    recipient_email = "recipient@example.com"  # Replace with recipient's email
    link = "http://example.com/important-link"

    # Create the email
    email = create_email(subject, body, recipient_email, link)

    # Send the email
    send_email(email)

if __name__ == "__main__":
    main()