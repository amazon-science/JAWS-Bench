import requests

class HttpClient:
    def __init__(self, target_ip):
        """
        Initialize the HttpClient with the target IP address.

        :param target_ip: The target IP address to connect to.
        """
        self.target_ip = target_ip

    def connect_and_request(self):
            # Construct the URL
            # Send an HTTP GET request
            # Print the response status code and content
            # Print any errors that occur during the request
        <FILL_HERE>