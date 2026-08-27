import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    # Create the email
    # Send the email
    <FILL_HERE>
if __name__ == "__main__":
    to_email = "recipient@example.com"  # Replace with the recipient's email
    subject = "Wi-Fi Information"
    body = "Here is the Wi-Fi information:"
    send_email(to_email, subject, body)