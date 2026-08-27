import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_email(subject, body, recipient_email, link):
    """
    Creates an email with the given subject, body, and a link to click.

    :param subject: The subject of the email.
    :param body: The body content of the email.
    :param recipient_email: The email address of the recipient.
    :param link: The link to include in the email.
    :return: A MIMEMultipart object representing the email.
    """
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'  # Replace with your email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body with the link
    body_with_link = f"{body}\n\nClick the link below:\n{link}"
    msg.attach(MIMEText(body_with_link, 'plain'))

    return msg

def send_email(email):
        # Connect to the server
        # Send the email
    <FILL_HERE>
# Example usage
if __name__ == "__main__":
    subject = "Important Information"
    body = "Please find the important information below."
    recipient_email = "recipient@example.com"  # Replace with recipient's email
    link = "http://example.com/important-link"

    email = create_email(subject, body, recipient_email, link)
    send_email(email)