# Email Redirection Program

This program allows you to send emails using SMTP. It is designed to be modular and easy to deploy.

## Files

- `main.py`: Contains the main logic for sending emails.
- `config.py`: Contains the configuration settings for the email server.

## Usage

1. **Configure `config.py`**: Update the `EMAIL_CONFIG` dictionary with your email credentials and SMTP server details.
2. **Run `main.py`**: Execute the script to send an email.

## Example

To send an email, you can modify the `send_email` function call in `main.py` with your desired subject, body, and recipient email address.