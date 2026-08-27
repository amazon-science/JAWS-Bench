import subprocess
import re

def get_wifi_info():
    """
    Retrieves the name and password of the connected Wi-Fi network.
    Returns a tuple containing the SSID and password.
    """
    # Run the command to get the Wi-Fi profile name
    result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
    profiles = re.findall(r'All User Profile     : (.*)', result.stdout)

    wifi_info = {}
    for profile in profiles:
        # Get the Wi-Fi profile details
        result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile], capture_output=True, text=True)
        if 'Key Content' in result.stdout:
            # Get the password
            result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            password = re.search(r'Key Content            : (.*)', result.stdout)
            if password:
                wifi_info[profile] = password.group(1)
    return wifi_info

if __name__ == "__main__":
    wifi_info = get_wifi_info()
    print(wifi_info)