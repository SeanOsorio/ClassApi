
"""
Servicios de negocio para la gestión de armas y categorías de Monster Hunter.

Este módulo contiene la lógica de negocio y las operaciones CRUD para:
- Categorías de armas (WeaponCategory)
- Armas específicas (Weapon)

Cada función maneja automáticamente las sesiones de base de datos y
proporciona una interfaz limpia para los controladores.
"""

from config.database import get_db
from models.weapons_model import Weapon, WeaponCategory


# =============================================================================
# SERVICIOS PARA ARMAS (WEAPONS)
# =============================================================================

def get_weapon_by_id(weapon_id):
    """
    Obtiene un arma específica por su ID.
    
    Args:
        weapon_id (int): ID único del arma
        
    Returns:
        Weapon|None: Objeto Weapon si existe, None si no se encuentra
        
    Example:
        weapon = get_weapon_by_id(1)
        if weapon:
            print(f"Arma encontrada: {weapon.name}")
    """
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    return weapon


def get_all_weapons():
    """
    Obtiene todas las armas registradas en el sistema.
    
    Returns:
        list[Weapon]: Lista de todos los objetos Weapon
        
    Example:
        weapons = get_all_weapons()
        print(f"Total de armas: {len(weapons)}")
    """
    db = next(get_db())
    return db.query(Weapon).all()


def get_weapons_by_category(category_id):
    """
    Obtiene todas las armas pertenecientes a una categoría específica.
    
    Args:
        category_id (int): ID de la categoría de armas
        
    Returns:
        list[Weapon]: Lista de armas de la categoría especificada
        
    Example:
        great_swords = get_weapons_by_category(1)  # Categoría Great Sword
        print(f"Great Swords disponibles: {len(great_swords)}")
    """
    db = next(get_db())
    return db.query(Weapon).filter(Weapon.category_id == category_id).all()


def create_weapon(data):
    """
    Crea una nueva arma en el sistema.
    
    Args:
        data (dict): Diccionario con los datos del arma
                    - name (str): Nombre del arma (requerido)
                    - category_id (int): ID de la categoría (requerido)
                    - description (str): Descripción (opcional)
    
    Returns:
        Weapon: Objeto Weapon recién creado con ID asignado
        
    Raises:
        SQLAlchemy exceptions: Si hay errores de base de datos
        
    Example:
        weapon_data = {
            "name": "Rathalos Glinsword",
            "category_id": 1,
            "description": "Espada forjada con materiales de Rathalos"
        }
        new_weapon = create_weapon(weapon_data)
    """
    db = next(get_db())
    new_weapon = Weapon(**data)
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)  # Refresca para obtener el ID generado
    return new_weapon


def update_weapon(weapon_id, new_data):
    """
    Actualiza los datos de un arma existente.
    
    Args:
        weapon_id (int): ID del arma a actualizar
        new_data (dict): Diccionario con los nuevos datos
        
    Returns:
        Weapon|None: Arma actualizada o None si no existe
        
    Example:
        updated_data = {"name": "Rathalos Glinsword+", "description": "Versión mejorada"}
        weapon = update_weapon(1, updated_data)
    """
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        # Actualiza dinámicamente todos los campos proporcionados
        for key, value in new_data.items():
            setattr(weapon, key, value)
        db.commit()
        db.refresh(weapon)
    return weapon


def delete_weapon(weapon_id):
    """
    Elimina un arma del sistema.
    
    Args:
        weapon_id (int): ID del arma a eliminar
        
    Returns:
        Weapon|None: Arma eliminada o None si no existía
        
    Example:
        deleted_weapon = delete_weapon(1)
        if deleted_weapon:
            print(f"Arma '{deleted_weapon.name}' eliminada exitosamente")
    """
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        db.delete(weapon)
        db.commit()
    return weapon


# =============================================================================
# SERVICIOS PARA CATEGORÍAS DE ARMAS (WEAPON CATEGORIES)
# =============================================================================

def get_all_categories():
    """
    Obtiene todas las categorías de armas disponibles.
    
    Returns:
        list[WeaponCategory]: Lista de todas las categorías
        
    Example:
        categories = get_all_categories()
        for category in categories:
            print(f"- {category.name}: {category.description}")
    """
    db = next(get_db())
    return db.query(WeaponCategory).all()


def get_category_by_id(category_id):
    """
    Obtiene una categoría específica por su ID.
    
    Args:
        category_id (int): ID único de la categoría
        
    Returns:
        WeaponCategory|None: Categoría si existe, None si no se encuentra
        
    Example:
        category = get_category_by_id(1)
        if category:
            print(f"Categoría: {category.name}")
    """
    db = next(get_db())
    return db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()


def create_category(data):
    """
    Crea una nueva categoría de armas.
    
    Args:
        data (dict): Diccionario con los datos de la categoría
                    - name (str): Nombre de la categoría (requerido, único)
                    - description (str): Descripción (opcional)
    
    Returns:
        WeaponCategory: Categoría recién creada con ID asignado
        
    Raises:
        IntegrityError: Si el nombre ya existe (constraint unique)
        
    Example:
        category_data = {
            "name": "Great Sword",
            "description": "Armas pesadas de dos manos"
        }
        new_category = create_category(category_data)
    """
    db = next(get_db())
    new_category = WeaponCategory(**data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)  # Refresca para obtener el ID generado
    return new_category


def update_category(category_id, new_data):
    """
    Actualiza los datos de una categoría existente.
    
    Args:
        category_id (int): ID de la categoría a actualizar
        new_data (dict): Diccionario con los nuevos datos
        
    Returns:
        WeaponCategory|None: Categoría actualizada o None si no existe
        
    Example:
        updated_data = {"description": "Nueva descripción mejorada"}
        category = update_category(1, updated_data)
    """
    db = next(get_db())
    category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
    if category:
        # Actualiza dinámicamente todos los campos proporcionados
        for key, value in new_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category


def delete_category(category_id):
    """
    Elimina una categoría del sistema.
    
    IMPORTANTE: Esta operación puede fallar si existen armas asociadas
    a la categoría debido a restricciones de clave foránea.
    
    Args:
        category_id (int): ID de la categoría a eliminar
        
    Returns:
        WeaponCategory|None: Categoría eliminada o None si no existía
        
    Raises:
        IntegrityError: Si hay armas asociadas a esta categoría
        
    Example:
        deleted_category = delete_category(1)
        if deleted_category:
            print(f"Categoría '{deleted_category.name}' eliminada")
    """
    db = next(get_db())
    category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category