
from flask import Blueprint, request, jsonify
from services.weapons_service import (
	get_all_categories, get_category_by_id, create_category, update_category, delete_category,
	get_weapon_by_id, create_weapon, update_weapon, delete_weapon
)

weapons_bp = Blueprint('weapons', __name__)

# --- Endpoints para categorías ---
# Obtener todas las categorías
@weapons_bp.route('/categories', methods=['GET'])
def list_categories():
	categories = get_all_categories()
	return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])

# Obtener una categoría por ID
@weapons_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
	category = get_category_by_id(category_id)
	if category:
		return jsonify({'id': category.id, 'name': category.name, 'description': category.description})
	return jsonify({'error': 'Categoría no encontrada'}), 404

# Crear una nueva categoría
@weapons_bp.route('/categories', methods=['POST'])
def create_new_category():
	data = request.json
	category = create_category(data)
	return jsonify({'id': category.id, 'name': category.name, 'description': category.description}), 201

# Actualizar una categoría
@weapons_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category_endpoint(category_id):
	data = request.json
	category = update_category(category_id, data)
	if category:
		return jsonify({'id': category.id, 'name': category.name, 'description': category.description})
	return jsonify({'error': 'Categoría no encontrada'}), 404

# Eliminar una categoría
@weapons_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_endpoint(category_id):
	category = delete_category(category_id)
	if category:
		return jsonify({'message': 'Categoría eliminada'})
	return jsonify({'error': 'Categoría no encontrada'}), 404

# --- Endpoints para armas (ejemplo básico) ---
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
	weapon = get_weapon_by_id(weapon_id)
	if weapon:
		return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description})
	return jsonify({'error': 'Arma no encontrada'}), 404

@weapons_bp.route('/weapons', methods=['POST'])
def create_new_weapon():
	data = request.json
	weapon = create_weapon(data)
	return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description}), 201

@weapons_bp.route('/weapons/<int:weapon_id>', methods=['PUT'])
def update_weapon_endpoint(weapon_id):
	data = request.json
	weapon = update_weapon(weapon_id, data)
	if weapon:
		return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description})
	return jsonify({'error': 'Arma no encontrada'}), 404

@weapons_bp.route('/weapons/<int:weapon_id>', methods=['DELETE'])
def delete_weapon_endpoint(weapon_id):
	weapon = delete_weapon(weapon_id)
	if weapon:
		return jsonify({'message': 'Arma eliminada'})
	return jsonify({'error': 'Arma no encontrada'}), 404
