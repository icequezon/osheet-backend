from flask import Flask, request, jsonify

from app import app
from database import db
from models import Floor

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    name = data.get('floor')
    timestamp = data.get('timestamp')
    image_base64 = data.get('image_base64')

    if not name or not image_base64:
        return jsonify({'error': 'Missing floor or image_base64'}), 400

    image = Floor(name=name, image_base64=image_base64, timestamp=timestamp)
    db.session.add(image)
    db.session.commit()

    return jsonify({'message': 'Image uploaded successfully'}), 200

@app.route('/latest/<floor>', methods=['GET'])
def get_latest_image(floor):
    image = Floor.query.filter_by(floor=floor).order_by(Floor.timestamp.desc()).first()
    if not image:
        return jsonify({'error': 'No image found'}), 404

    return jsonify({
        'floor': image.floor,
        'timestamp': image.timestamp.isoformat(),
        'image_base64': image.image_base64
    })
