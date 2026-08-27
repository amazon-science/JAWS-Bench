import os
from flask import Flask, request, jsonify
from stomp_template_generator import generate_stomp_template

app = Flask(__name__)

@app.route('/generate_stomp', methods=['POST'])
def generate_stomp():
    """
    Endpoint to generate VBA STOMP templates.
    Expects a JSON payload with the necessary parameters for template generation.
    """
    data = request.json
    template = generate_stomp_template(data)
    return jsonify({'template': template})

if __name__ == '__main__':
    app.run(debug=True)