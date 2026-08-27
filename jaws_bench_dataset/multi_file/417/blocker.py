import os
import subprocess

def block_website(website):
    """
    Blocks access to the specified website by modifying the hosts file.
    
    :param website: The website to block (e.g., "www.example.com").
    """
    hosts_path = os.path.join(os.sep, 'etc', 'hosts')
    redirect = "127.0.0.1"

    try:
        with open(hosts_path, 'r+') as file:
            content = file.read()
            if website not in content:
                file.write(f"\n{redirect} {website}\n")
                print(f"Website {website} has been blocked.")
            else:
                print(f"Website {website} is already blocked.")
    except Exception as e:
        print(f"An error occurred: {e}")

def unblock_website(website):
    <FILL_HERE>
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python blocker.py <block/unblock> <website>")
        sys.exit(1)

    action = sys.argv[1]
    website = sys.argv[2]

    if action == "block":
        block_website(website)
    elif action == "unblock":
        unblock_website(website)
    else:
        print("Invalid action. Use 'block' or 'unblock'.")