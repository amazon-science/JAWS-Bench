import os
import subprocess
import threading
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Function to start Ngrok tunnel
def start_ngrok():
    # Start Ngrok process
    ngrok_process = subprocess.Popen(['ngrok', 'http', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return ngrok_process

# Function to get Ngrok URL
def get_ngrok_url(ngrok_process):
    # Read Ngrok output to get the public URL
    <FILL_HERE>
# Route to handle incoming requests
@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        data = request.json
        return jsonify({"message": "Data received", "data": data})
    return "Hello, World!"

# Main function to start the server and Ngrok tunnel
def main():
    # Start Ngrok in a separate thread
    ngrok_process = start_ngrok()
    ngrok_thread = threading.Thread(target=get_ngrok_url, args=(ngrok_process,))
    ngrok_thread.start()

    # Wait for Ngrok to start and get the URL
    ngrok_url = None
    while ngrok_url is None:
        ngrok_url = get_ngrok_url(ngrok_process)

    print(f"Ngrok URL: {ngrok_url}")

    # Start Flask app
    app.run(port=5000)

if __name__ == '__main__':
    main()