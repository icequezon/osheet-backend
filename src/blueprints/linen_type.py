from flask import request, jsonify, Blueprint

from .services import LinenTypeService
from .serializers import LinenTypeSerializer

app = Blueprint('linen_type', __name__, url_prefix='/linen_type')

@app.route('/', methods=['POST'])
def create_new_linen_type():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Missing linen name'}), 400

    LinenTypeService.create(name)
    return jsonify({'message': 'LinenType created successfully'}), 200

@app.route('/', methods=['GET'])
def get_all_floors():
    floors = LinenTypeService.get_all_linen_types()
    return jsonify(LinenTypeSerializer().serializeMany(floors)), 200

@app.route('/<id>', methods=['GET'])
def get_floor(id):
    try:
        floor = LinenTypeService.get(id)
        return jsonify(LinenTypeSerializer().serialize(floor)), 200
    except Exception as e:
        return jsonify({"error": e.args[0]}), 404

@app.route('/<id>', methods=["DELETE"])
def delete_floor(id):
    if not id:
        return jsonify({'error': 'Missing id'}), 400
    LinenTypeService.delete(id)
    return jsonify({'message': 'LinenType deleted successfully'}), 200
