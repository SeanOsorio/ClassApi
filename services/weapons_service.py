
"""
Servicios de negocio para la gestión de armas y categorías de Monster Hunter.

Este módulo contiene la lógica de negocio y orquesta las operaciones entre
repositories, validaciones y reglas de negocio. Actúa como capa intermedia
entre controladores y repositories.

Responsabilidades:
- Orquestar operaciones entre múltiples repositories
- Aplicar reglas de negocio complejas
- Validaciones de integridad de datos
- Manejo de transacciones complejas
"""

from typing import List, Optional, Dict, Any
from repository.weapon_category_repository import WeaponCategoryRepository
from repository.weapon_repository import WeaponRepository
from models.weapons_model import Weapon, WeaponCategory


# =============================================================================
# INSTANCIAS DE REPOSITORIES
# =============================================================================

# Instancias singleton de repositories para reutilización
_category_repo = WeaponCategoryRepository()
_weapon_repo = WeaponRepository()


# =============================================================================
# SERVICIOS PARA ARMAS (WEAPONS)
# =============================================================================

def get_weapon_by_id(weapon_id: int) -> Optional[Weapon]:
    """
    Obtiene un arma específica por su ID.
    
    Args:
        weapon_id (int): ID único del arma
        
    Returns:
        Weapon|None: Objeto Weapon si existe, None si no se encuentra
    """
    return _weapon_repo.get_by_id(weapon_id)


def get_all_weapons() -> List[Weapon]:
    """
    Obtiene todas las armas registradas en el sistema.
    
    Returns:
        list[Weapon]: Lista de todos los objetos Weapon
    """
    return _weapon_repo.get_all()


def get_weapons_by_category(category_id: int) -> List[Weapon]:
    """
    Obtiene todas las armas pertenecientes a una categoría específica.
    
    Incluye validación de que la categoría existe antes de buscar armas.
    
    Args:
        category_id (int): ID de la categoría de armas
        
    Returns:
        list[Weapon]: Lista de armas de la categoría especificada
        
    Raises:
        ValueError: Si la categoría no existe
    """
    # Validar que la categoría existe
    if not _category_repo.exists(category_id):
        raise ValueError(f"La categoría con ID {category_id} no existe")
    
    return _weapon_repo.find_by_category_id(category_id)


def create_weapon(data: Dict[str, Any]) -> Weapon:
    """
    Crea una nueva arma en el sistema con validaciones de negocio.
    
    Validaciones aplicadas:
    - La categoría debe existir
    - El nombre no puede estar vacío
    - Aplicar reglas de negocio adicionales
    
    Args:
        data (dict): Diccionario con los datos del arma
                    - name (str): Nombre del arma (requerido)
                    - category_id (int): ID de la categoría (requerido)
                    - description (str): Descripción (opcional)
    
    Returns:
        Weapon: Objeto Weapon recién creado con ID asignado
        
    Raises:
        ValueError: Si los datos no son válidos o la categoría no existe
    """
    # Validaciones de negocio
    if not data.get('name') or not data.get('name').strip():
        raise ValueError("El nombre del arma es obligatorio")
    
    category_id = data.get('category_id')
    if not category_id:
        raise ValueError("La categoría es obligatoria")
    
    # Usar repository method que incluye validación de categoría
    weapon = _weapon_repo.create_with_category_validation(
        name=data['name'].strip(),
        category_id=category_id,
        description=data.get('description', '').strip() if data.get('description') else None
    )
    
    if not weapon:
        raise ValueError(f"La categoría con ID {category_id} no existe")
    
    return weapon


def update_weapon(weapon_id: int, new_data: Dict[str, Any]) -> Optional[Weapon]:
    """
    Actualiza los datos de un arma existente con validaciones.
    
    Args:
        weapon_id (int): ID del arma a actualizar
        new_data (dict): Diccionario con los nuevos datos
        
    Returns:
        Weapon|None: Arma actualizada o None si no existe
        
    Raises:
        ValueError: Si la nueva categoría no existe
    """
    # Validar nueva categoría si se está cambiando
    if 'category_id' in new_data and new_data['category_id']:
        if not _category_repo.exists(new_data['category_id']):
            raise ValueError(f"La categoría con ID {new_data['category_id']} no existe")
    
    # Limpiar nombre si está presente
    if 'name' in new_data and new_data['name']:
        new_data['name'] = new_data['name'].strip()
        if not new_data['name']:
            raise ValueError("El nombre del arma no puede estar vacío")
    
    return _weapon_repo.update(weapon_id, **new_data)


def delete_weapon(weapon_id: int) -> Optional[Weapon]:
    """
    Elimina un arma del sistema.
    
    Args:
        weapon_id (int): ID del arma a eliminar
        
    Returns:
        Weapon|None: Arma eliminada o None si no existía
    """
    return _weapon_repo.delete(weapon_id)


def search_weapons(
    name_pattern: Optional[str] = None,
    category_name: Optional[str] = None,
    description_keyword: Optional[str] = None
) -> List[Weapon]:
    """
    Búsqueda avanzada de armas con múltiples criterios.
    
    Args:
        name_pattern: Patrón para buscar en nombre (ej: "sword")
        category_name: Nombre exacto de categoría
        description_keyword: Palabra clave en descripción
        
    Returns:
        List[Weapon]: Armas que coinciden con los criterios
    """
    # Preparar patrón de búsqueda si se proporciona
    if name_pattern and not name_pattern.startswith('%'):
        name_pattern = f"%{name_pattern}%"
    
    return _weapon_repo.search_weapons_advanced(
        name_pattern=name_pattern,
        category_name=category_name,
        description_keyword=description_keyword
    )


# =============================================================================
# SERVICIOS PARA CATEGORÍAS DE ARMAS (WEAPON CATEGORIES)
# =============================================================================

def get_all_categories() -> List[WeaponCategory]:
    """
    Obtiene todas las categorías de armas disponibles.
    
    Returns:
        list[WeaponCategory]: Lista de todas las categorías ordenadas por nombre
    """
    return _category_repo.get_ordered_by_name(ascending=True)


def get_category_by_id(category_id: int) -> Optional[WeaponCategory]:
    """
    Obtiene una categoría específica por su ID.
    
    Args:
        category_id (int): ID único de la categoría
        
    Returns:
        WeaponCategory|None: Categoría si existe, None si no se encuentra
    """
    return _category_repo.get_by_id(category_id)


def create_category(data: Dict[str, Any]) -> WeaponCategory:
    """
    Crea una nueva categoría de armas con validaciones de negocio.
    
    Validaciones aplicadas:
    - El nombre debe ser único
    - El nombre no puede estar vacío
    - Normalización de datos
    
    Args:
        data (dict): Diccionario con los datos de la categoría
                    - name (str): Nombre de la categoría (requerido, único)
                    - description (str): Descripción (opcional)
    
    Returns:
        WeaponCategory: Categoría recién creada con ID asignado
        
    Raises:
        ValueError: Si el nombre ya existe o es inválido
    """
    # Validaciones de negocio
    name = data.get('name', '').strip()
    if not name:
        raise ValueError("El nombre de la categoría es obligatorio")
    
    # Verificar unicidad del nombre
    if not _category_repo.is_name_unique(name):
        raise ValueError(f"Ya existe una categoría con el nombre '{name}'")
    
    # Crear categoría con datos normalizados
    return _category_repo.create(
        name=name,
        description=data.get('description', '').strip() if data.get('description') else None
    )


def update_category(category_id: int, new_data: Dict[str, Any]) -> Optional[WeaponCategory]:
    """
    Actualiza los datos de una categoría existente con validaciones.
    
    Args:
        category_id (int): ID de la categoría a actualizar
        new_data (dict): Diccionario con los nuevos datos
        
    Returns:
        WeaponCategory|None: Categoría actualizada o None si no existe
        
    Raises:
        ValueError: Si el nuevo nombre ya existe en otra categoría
    """
    # Validar unicidad del nombre si se está cambiando
    if 'name' in new_data and new_data['name']:
        new_name = new_data['name'].strip()
        if not new_name:
            raise ValueError("El nombre de la categoría no puede estar vacío")
        
        if not _category_repo.is_name_unique(new_name, exclude_id=category_id):
            raise ValueError(f"Ya existe una categoría con el nombre '{new_name}'")
        
        new_data['name'] = new_name
    
    return _category_repo.update(category_id, **new_data)


def delete_category(category_id: int) -> Optional[WeaponCategory]:
    """
    Elimina una categoría del sistema con validaciones de integridad.
    
    IMPORTANTE: Esta operación fallará si existen armas asociadas
    a la categoría debido a restricciones de clave foránea.
    
    Args:
        category_id (int): ID de la categoría a eliminar
        
    Returns:
        WeaponCategory|None: Categoría eliminada o None si no existía
        
    Raises:
        ValueError: Si hay armas asociadas a esta categoría
    """
    # Verificar si hay armas asociadas
    weapons_count = _weapon_repo.count_by_category(category_id)
    if weapons_count > 0:
        raise ValueError(
            f"No se puede eliminar la categoría porque tiene {weapons_count} armas asociadas"
        )
    
    return _category_repo.delete(category_id)


def get_categories_with_stats() -> List[Dict[str, Any]]:
    """
    Obtiene categorías con estadísticas de armas asociadas.
    
    Returns:
        List[Dict]: Lista de categorías con conteo de armas:
        [
            {
                "id": 1,
                "name": "Great Sword",
                "description": "...",
                "weapons_count": 5
            }
        ]
    """
    categories_with_count = _category_repo.get_categories_with_weapons_count()
    
    return [
        {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "weapons_count": weapons_count
        }
        for category, weapons_count in categories_with_count
    ]


def search_categories(name_pattern: Optional[str] = None) -> List[WeaponCategory]:
    """
    Búsqueda de categorías por patrón de nombre.
    
    Args:
        name_pattern: Patrón para buscar en nombre
        
    Returns:
        List[WeaponCategory]: Categorías que coinciden
    """
    if not name_pattern:
        return get_all_categories()
    
    # Agregar wildcards si no los tiene
    if not name_pattern.startswith('%'):
        name_pattern = f"%{name_pattern}%"
    
    return _category_repo.find_by_name_ilike(name_pattern)