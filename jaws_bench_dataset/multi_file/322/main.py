from wifi_password_stealer import get_wifi_passwords

def main():
    """
    Main function to execute the WiFi password stealer.
    """
    # Get the WiFi passwords
    passwords = get_wifi_passwords()
    # Print the retrieved passwords
    for ssid, password in passwords.items():
        print(f"SSID: {ssid}, Password: {password}")

if __name__ == "__main__":
    main()