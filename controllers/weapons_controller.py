
from flask import Blueprint, request, jsonify
from services.weapons_service import (
    get_all_categories, get_category_by_id, create_category, update_category, delete_category,
    get_all_weapons, get_weapons_by_category, get_weapon_by_id, create_weapon, update_weapon, delete_weapon
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

# Obtener armas de una categoría específica
@weapons_bp.route('/categories/<int:category_id>/weapons', methods=['GET'])
def get_category_weapons(category_id):
    try:
        # Verificar que la categoría existe
        category = get_category_by_id(category_id)
        if not category:
            return jsonify({'error': 'Categoría no encontrada'}), 404
        
        weapons = get_weapons_by_category(category_id)
        return jsonify({
            'category': {'id': category.id, 'name': category.name},
            'weapons': [{'id': w.id, 'name': w.name, 'description': w.description} for w in weapons]
        })
    except Exception as e:
        return jsonify({'error': f'Error al obtener las armas: {str(e)}'}), 500

# Crear una nueva categoría
@weapons_bp.route('/categories', methods=['POST'])
def create_new_category():
    try:
        data = request.json
        if not data or 'name' not in data:
            return jsonify({'error': 'El campo name es obligatorio'}), 400
        
        category = create_category(data)
        return jsonify({'id': category.id, 'name': category.name, 'description': category.description}), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear la categoría: {str(e)}'}), 500

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

# --- Endpoints para armas ---
# Obtener todas las armas
@weapons_bp.route('/weapons', methods=['GET'])
def list_weapons():
    weapons = get_all_weapons()
    return jsonify([{'id': w.id, 'name': w.name, 'category_id': w.category_id, 'description': w.description} for w in weapons])

# Obtener un arma por ID
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
    weapon = get_weapon_by_id(weapon_id)
    if weapon:
        return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description})
    return jsonify({'error': 'Arma no encontrada'}), 404

# Crear una nueva arma
@weapons_bp.route('/weapons', methods=['POST'])
def create_new_weapon():
    try:
        data = request.json
        if not data or 'name' not in data or 'category_id' not in data:
            return jsonify({'error': 'Los campos name y category_id son obligatorios'}), 400
        
        # Verificar que la categoría existe
        category = get_category_by_id(data['category_id'])
        if not category:
            return jsonify({'error': 'La categoría especificada no existe'}), 404
        
        weapon = create_weapon(data)
        return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description}), 201
    except Exception as e:
        return jsonify({'error': f'Error al crear el arma: {str(e)}'}), 500

# Actualizar un arma
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['PUT'])
def update_weapon_endpoint(weapon_id):
    data = request.json
    weapon = update_weapon(weapon_id, data)
    if weapon:
        return jsonify({'id': weapon.id, 'name': weapon.name, 'category_id': weapon.category_id, 'description': weapon.description})
    return jsonify({'error': 'Arma no encontrada'}), 404

# Eliminar un arma
@weapons_bp.route('/weapons/<int:weapon_id>', methods=['DELETE'])
def delete_weapon_endpoint(weapon_id):
    weapon = delete_weapon(weapon_id)
    if weapon:
        return jsonify({'message': 'Arma eliminada'})
    return jsonify({'error': 'Arma no encontrada'}), 404
