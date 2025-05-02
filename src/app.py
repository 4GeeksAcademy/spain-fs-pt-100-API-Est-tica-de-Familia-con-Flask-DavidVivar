"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1. GET /members - Obtener todos los miembros
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# 2. GET /members/<int:member_id> - Obtener un miembro específico
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"msg": "Miembro no encontrado"}), 404
    return jsonify(member), 200

# 3. POST /members - Agregar un nuevo miembro
@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"msg": "Datos incompletos"}), 400

    jackson_family.add_member(data)
    return jsonify({"msg": "Miembro agregado exitosamente"}), 200

# 4. DELETE /members/<int:member_id> - Eliminar un miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"msg": "Miembro no encontrado"}), 404
    jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200

# Run the server
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
