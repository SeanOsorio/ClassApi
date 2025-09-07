
"""
Controladores REST para la API de armas de Monster Hunter.

Este módulo define todos los endpoints HTTP para la gestión de:
- Categorías de armas (/categories)
- Armas específicas (/weapons)

Incluye validaciones, manejo de errores y respuestas HTTP apropiadas
siguiendo las mejores prácticas de APIs RESTful.

Endpoints disponibles:
- GET    /categories              -> Listar todas las categorías
- GET    /categories/{id}         -> Obtener categoría por ID
- GET    /categories/{id}/weapons -> Listar armas de una categoría
- POST   /categories              -> Crear nueva categoría
- PUT    /categories/{id}         -> Actualizar categoría
- DELETE /categories/{id}         -> Eliminar categoría
- GET    /weapons                 -> Listar todas las armas
- GET    /weapons/{id}            -> Obtener arma por ID
- POST   /weapons                 -> Crear nueva arma
- PUT    /weapons/{id}            -> Actualizar arma
- DELETE /weapons/{id}            -> Eliminar arma
"""

from flask import Blueprint, request, jsonify
from services.weapons_service import (
    get_all_categories, get_category_by_id, create_category, update_category, delete_category,
    get_all_weapons, get_weapons_by_category, get_weapon_by_id, create_weapon, update_weapon, delete_weapon
)

# Blueprint para agrupar todas las rutas relacionadas con armas
weapons_bp = Blueprint('weapons', __name__)


# =============================================================================
# ENDPOINTS PARA CATEGORÍAS DE ARMAS
# =============================================================================

@weapons_bp.route('/categories', methods=['GET'])
def list_categories():
    """
    Obtiene la lista completa de categorías de armas disponibles.
    
    Returns:
        JSON: Lista de categorías con estructura:
        [
            {
                "id": 1,
                "name": "Great Sword",
                "description": "Armas pesadas de dos manos..."
            }
        ]
        
    Status Codes:
        200: Éxito - Lista retornada correctamente
        500: Error interno del servidor
    """
    categories = get_all_categories()
    return jsonify([
        {
            'id': c.id, 
            'name': c.name, 
            'description': c.description
        } for c in categories
    ])


@weapons_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Obtiene los detalles de una categoría específica por su ID.
    
    Args:
        category_id (int): ID único de la categoría
        
    Returns:
        JSON: Datos de la categoría o mensaje de error
        
    Status Codes:
        200: Categoría encontrada
        404: Categoría no existe
    """
    category = get_category_by_id(category_id)
    if category:
        return jsonify({
            'id': category.id, 
            'name': category.name, 
            'description': category.description
        })
    return jsonify({'error': 'Categoría no encontrada'}), 404


@weapons_bp.route('/categories/<int:category_id>/weapons', methods=['GET'])
def get_category_weapons(category_id):
    """
    Obtiene todas las armas pertenecientes a una categoría específica.
    
    Este endpoint es útil para mostrar todas las variantes de armas
    dentro de un tipo específico (ej: todas las Great Swords).
    
    Args:
        category_id (int): ID de la categoría de armas
        
    Returns:
        JSON: Información de la categoría y sus armas asociadas:
        {
            "category": {"id": 1, "name": "Great Sword"},
            "weapons": [
                {"id": 1, "name": "Buster Sword", "description": "..."},
                {"id": 2, "name": "Chrome Razor", "description": "..."}
            ]
        }
        
    Status Codes:
        200: Éxito - Lista de armas retornada
        404: Categoría no existe
        500: Error interno del servidor
    """
    try:
        # Validar existencia de la categoría antes de buscar armas
        category = get_category_by_id(category_id)
        if not category:
            return jsonify({'error': 'Categoría no encontrada'}), 404
        
        weapons = get_weapons_by_category(category_id)
        return jsonify({
            'category': {'id': category.id, 'name': category.name},
            'weapons': [
                {
                    'id': w.id, 
                    'name': w.name, 
                    'description': w.description
                } for w in weapons
            ]
        })
    except Exception as e:
        return jsonify({'error': f'Error al obtener las armas: {str(e)}'}), 500


@weapons_bp.route('/categories', methods=['POST'])
def create_new_category():
    """
    Crea una nueva categoría de armas.
    
    Body JSON requerido:
        {
            "name": "Nombre de la categoría" (requerido),
            "description": "Descripción detallada" (opcional)
        }
        
    Returns:
        JSON: Categoría creada con ID asignado
        
    Status Codes:
        201: Categoría creada exitosamente
        400: Datos de entrada inválidos
        500: Error interno del servidor (ej: nombre duplicado)
        
    Example:
        POST /categories
        {
            "name": "Switch Axe",
            "description": "Arma transformable entre modo hacha y espada"
        }
    """
    try:
        data = request.json
        
        # Validar estructura del JSON
        if not data or 'name' not in data:
            return jsonify({'error': 'El campo name es obligatorio'}), 400
        
        category = create_category(data)
        return jsonify({
            'id': category.id, 
            'name': category.name, 
            'description': category.description
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error al crear la categoría: {str(e)}'}), 500


@weapons_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category_endpoint(category_id):
    """
    Actualiza los datos de una categoría existente.
    
    Args:
        category_id (int): ID de la categoría a actualizar
        
    Body JSON:
        {
            "name": "Nuevo nombre" (opcional),
            "description": "Nueva descripción" (opcional)
        }
        
    Returns:
        JSON: Categoría actualizada
        
    Status Codes:
        200: Actualización exitosa
        404: Categoría no existe
        500: Error interno del servidor
    """
    data = request.json
    category = update_category(category_id, data)
    if category:
        return jsonify({
            'id': category.id, 
            'name': category.name, 
            'description': category.description
        })
    return jsonify({'error': 'Categoría no encontrada'}), 404


@weapons_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_endpoint(category_id):
    """
    Elimina una categoría del sistema.
    
    IMPORTANTE: Esta operación fallará si existen armas asociadas
    a la categoría debido a restricciones de integridad referencial.
    
    Args:
        category_id (int): ID de la categoría a eliminar
        
    Returns:
        JSON: Mensaje de confirmación o error
        
    Status Codes:
        200: Eliminación exitosa
        404: Categoría no existe
        500: Error de integridad (armas asociadas)
    """
    category = delete_category(category_id)
    if category:
        return jsonify({'message': 'Categoría eliminada'})
    return jsonify({'error': 'Categoría no encontrada'}), 404


# =============================================================================
# ENDPOINTS PARA ARMAS ESPECÍFICAS
# =============================================================================

@weapons_bp.route('/weapons', methods=['GET'])
def list_weapons():
    """
    Obtiene la lista completa de todas las armas registradas.
    
    Returns:
        JSON: Lista de armas con información básica:
        [
            {
                "id": 1,
                "name": "Rathalos Glinsword",
                "category_id": 1,
                "description": "Espada forjada con materiales de Rathalos"
            }
        ]
        
    Status Codes:
        200: Lista retornada correctamente
    """
    weapons = get_all_weapons()
    return jsonify([
        {
            'id': w.id, 
            'name': w.name, 
            'category_id': w.category_id, 
            'description': w.description
        } for w in weapons
    ])


@weapons_bp.route('/weapons/<int:weapon_id>', methods=['GET'])
def get_weapon(weapon_id):
    """
    Obtiene los detalles de un arma específica por su ID.
    
    Args:
        weapon_id (int): ID único del arma
        
    Returns:
        JSON: Datos del arma o mensaje de error
        
    Status Codes:
        200: Arma encontrada
        404: Arma no existe
    """
    weapon = get_weapon_by_id(weapon_id)
    if weapon:
        return jsonify({
            'id': weapon.id, 
            'name': weapon.name, 
            'category_id': weapon.category_id, 
            'description': weapon.description
        })
    return jsonify({'error': 'Arma no encontrada'}), 404


@weapons_bp.route('/weapons', methods=['POST'])
def create_new_weapon():
    """
    Crea una nueva arma en el sistema.
    
    Body JSON requerido:
        {
            "name": "Nombre del arma" (requerido),
            "category_id": 1 (requerido),
            "description": "Descripción del arma" (opcional)
        }
        
    Validaciones:
        - name: Campo obligatorio
        - category_id: Campo obligatorio y debe existir la categoría
        - description: Campo opcional
        
    Returns:
        JSON: Arma creada con ID asignado
        
    Status Codes:
        201: Arma creada exitosamente
        400: Datos de entrada inválidos
        404: Categoría especificada no existe
        500: Error interno del servidor
        
    Example:
        POST /weapons
        {
            "name": "Fire and Ice",
            "category_id": 4,
            "description": "Espadas duales con elementos opuestos"
        }
    """
    try:
        data = request.json
        
        # Validar campos requeridos
        if not data or 'name' not in data or 'category_id' not in data:
            return jsonify({
                'error': 'Los campos name y category_id son obligatorios'
            }), 400
        
        # Validar que la categoría existe (integridad referencial)
        category = get_category_by_id(data['category_id'])
        if not category:
            return jsonify({
                'error': 'La categoría especificada no existe'
            }), 404
        
        weapon = create_weapon(data)
        return jsonify({
            'id': weapon.id, 
            'name': weapon.name, 
            'category_id': weapon.category_id, 
            'description': weapon.description
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error al crear el arma: {str(e)}'}), 500


@weapons_bp.route('/weapons/<int:weapon_id>', methods=['PUT'])
def update_weapon_endpoint(weapon_id):
    """
    Actualiza los datos de un arma existente.
    
    Args:
        weapon_id (int): ID del arma a actualizar
        
    Body JSON:
        {
            "name": "Nuevo nombre" (opcional),
            "category_id": 2 (opcional),
            "description": "Nueva descripción" (opcional)
        }
        
    Returns:
        JSON: Arma actualizada
        
    Status Codes:
        200: Actualización exitosa
        404: Arma no existe
        500: Error interno del servidor
    """
    data = request.json
    weapon = update_weapon(weapon_id, data)
    if weapon:
        return jsonify({
            'id': weapon.id, 
            'name': weapon.name, 
            'category_id': weapon.category_id, 
            'description': weapon.description
        })
    return jsonify({'error': 'Arma no encontrada'}), 404


@weapons_bp.route('/weapons/<int:weapon_id>', methods=['DELETE'])
def delete_weapon_endpoint(weapon_id):
    """
    Elimina un arma del sistema.
    
    Args:
        weapon_id (int): ID del arma a eliminar
        
    Returns:
        JSON: Mensaje de confirmación o error
        
    Status Codes:
        200: Eliminación exitosa
        404: Arma no existe
    """
    weapon = delete_weapon(weapon_id)
    if weapon:
        return jsonify({'message': 'Arma eliminada'})
    return jsonify({'error': 'Arma no encontrada'}), 404
