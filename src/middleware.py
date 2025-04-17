import os
from flask import request, jsonify

def check_api_key():
    sent_api_key = request.headers.get('X-Api-Key')
    API_KEY = os.getenv('API_KEY')

    if sent_api_key or sent_api_key != API_KEY:
        return jsonify({"error": "Unautorized"}), 401
