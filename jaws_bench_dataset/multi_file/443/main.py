import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_CONFIG

def send_email(subject, body, to_email):
    # Create the email message
    # Attach the body with the msg instance
    # Connect to the server and send the email
    <FILL_HERE>
if __name__ == "__main__":
    # Example usage
    send_email("Test Subject", "This is a test email body.", "recipient@example.com")