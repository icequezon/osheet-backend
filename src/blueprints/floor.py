from flask import request, jsonify, Blueprint

from .services import FloorService
from .serializers import FloorSerializer

app = Blueprint('floor', __name__, url_prefix='/floor')

@app.route('/', methods=['POST'])
def create_new_floor():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Missing floor name'}), 400

    FloorService.create(name)
    return jsonify({'message': 'Floor created successfully'}), 200

@app.route('/', methods=['GET'])
def get_all_floors():
    floors = FloorService.get_all_floors()
    return jsonify(FloorSerializer().serializeMany(floors)), 200

@app.route('/<id>', methods=['GET'])
def get_floor(id):
    try:
        floor = FloorService.get(id)
        return jsonify(FloorSerializer().serialize(floor)), 200
    except Exception as e:
        return jsonify({"error": e.args[0]}), 404

@app.route('/<id>', methods=["DELETE"])
def delete_floor(id):
    if not id:
        return jsonify({'error': 'Missing id'}), 400
    FloorService.delete(id)
    return jsonify({'message': 'Floor deleted successfully'}), 200


@app.route('/<id>/update_image', methods=['POST'])
def update_image(id):
    data = request.get_json()
    timestamp = data.get('timestamp')
    image_base64 = data.get('image_base64')

    if not id or not image_base64 or not timestamp:
        return jsonify({'error': 'Missing floor or image_base64 or timestamp'}), 400

    try:
        FloorService.update_image(id, image_base64, timestamp)
        return jsonify({'message': 'Image uploaded successfully'}), 200
    except Exception as e:
        return jsonify({"error": e.args[0]}), 404

@app.route('/<id>/add_linen', methods=['POST'])
def add_linen(id):
    data = request.get_json()
    linen_type_id = data.get('linen_type_id')

    if not linen_type_id:
        return jsonify({'error': 'Missing linen_type_id'}), 400

    try:
        FloorService.add_linen(id, linen_type_id=linen_type_id)
        return jsonify({'message': 'Linen Type added to floor successfully'}), 200
    except Exception as e:
        return jsonify({"error": e.args[0]}), 404

@app.route('/<id>/remove_linen', methods=['POST'])
def remove_linen(id):
    data = request.get_json()
    floor_linen_id = data.get('floor_linen_id')

    if not floor_linen_id:
        return jsonify({'error': 'Missing floor_linen_id'}), 400

    try:
        FloorService.remove_linen(id, floor_linen_id=floor_linen_id)
        return jsonify({'message': 'Floor Linen removed from floor successfully'}), 200
    except Exception as e:
        return jsonify({"error": e.args[0]}), 404
