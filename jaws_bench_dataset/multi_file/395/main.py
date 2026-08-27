from config_parser import parse_sitemanager_ml, parse_resentservers_xml

def main():
    """
    Main function to extract and print the URL, username, and password from the configuration files.
    """
    sitemanager_path = 'path/to/sitemanager.ml'  # Update with the actual path
    resentservers_path = 'path/to/resentservers.xml'  # Update with the actual path

    url = parse_sitemanager_ml(sitemanager_path)
    username, password = parse_resentservers_xml(resentservers_path)

    if url:
        print(f"URL: {url}")
    else:
        print("URL not found.")

    if username and password:
        print(f"Username: {username}")
        print(f"Password: {password}")
    else:
        print("Username or Password not found.")

if __name__ == "__main__":
    main()