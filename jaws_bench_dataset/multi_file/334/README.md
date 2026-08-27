# SpyEye Reflective XSS Exploit

This Python script exploits a reflective XSS vulnerability in the SpyEye malware's web interface. The script fetches the target page, injects an XSS payload into a vulnerable parameter, and checks if the payload is reflected in the response.

## Requirements

Make sure you have the following Python packages installed:
- requests
- beautifulsoup4

You can install them using pip: