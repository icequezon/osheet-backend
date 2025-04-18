from flask import request, jsonify
from .config import API_KEY


def check_api_key():
    sent_api_key = request.headers.get('X-Api-Key')

    if not sent_api_key or sent_api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
