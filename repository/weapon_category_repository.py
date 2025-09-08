"""
Repository para el manejo de categorías de armas.

Este módulo contiene toda la lógica de acceso a datos específica
para la entidad WeaponCategory, incluyendo operaciones CRUD
y consultas especializadas.
"""

from typing import List, Optional
from sqlalchemy import and_
from models.weapons_model import WeaponCategory
from repository.base_repository import BaseRepository


class WeaponCategoryRepository(BaseRepository[WeaponCategory]):
    """
    Repository específico para categorías de armas.
    
    Hereda operaciones CRUD básicas de BaseRepository y añade
    funcionalidades específicas para categorías de armas.
    """
    
    def __init__(self):
        """Inicializa el repository con el modelo WeaponCategory."""
        super().__init__(WeaponCategory)
    
    def find_by_name(self, name: str) -> Optional[WeaponCategory]:
        """
        Busca una categoría por su nombre exacto.
        
        Args:
            name: Nombre de la categoría a buscar
            
        Returns:
            Optional[WeaponCategory]: Categoría si existe, None si no se encuentra
            
        Example:
            category = repo.find_by_name("Great Sword")
        """
        db = self._get_db()
        return db.query(WeaponCategory).filter(
            WeaponCategory.name == name
        ).first()
    
    def find_by_name_ilike(self, name_pattern: str) -> List[WeaponCategory]:
        """
        Busca categorías por patrón de nombre (case-insensitive).
        
        Args:
            name_pattern: Patrón de búsqueda (ej: "%sword%")
            
        Returns:
            List[WeaponCategory]: Lista de categorías que coinciden
            
        Example:
            categories = repo.find_by_name_ilike("%sword%")
        """
        db = self._get_db()
        return db.query(WeaponCategory).filter(
            WeaponCategory.name.ilike(name_pattern)
        ).all()
    
    def search_by_description(self, keyword: str) -> List[WeaponCategory]:
        """
        Busca categorías por palabra clave en la descripción.
        
        Args:
            keyword: Palabra clave a buscar en descripción
            
        Returns:
            List[WeaponCategory]: Categorías con la palabra en descripción
            
        Example:
            categories = repo.search_by_description("pesada")
        """
        db = self._get_db()
        return db.query(WeaponCategory).filter(
            WeaponCategory.description.ilike(f"%{keyword}%")
        ).all()
    
    def get_categories_with_weapons_count(self) -> List[tuple]:
        """
        Obtiene categorías con el conteo de armas asociadas.
        
        Returns:
            List[tuple]: Lista de (WeaponCategory, count) tuplas
            
        Example:
            for category, weapon_count in repo.get_categories_with_weapons_count():
                print(f"{category.name}: {weapon_count} armas")
        """
        from models.weapons_model import Weapon
        
        db = self._get_db()
        return db.query(WeaponCategory, db.func.count(Weapon.id).label('weapon_count'))\
                 .outerjoin(Weapon, WeaponCategory.id == Weapon.category_id)\
                 .group_by(WeaponCategory.id)\
                 .all()
    
    def get_categories_without_weapons(self) -> List[WeaponCategory]:
        """
        Obtiene categorías que no tienen armas asociadas.
        
        Returns:
            List[WeaponCategory]: Categorías sin armas
            
        Example:
            empty_categories = repo.get_categories_without_weapons()
        """
        from models.weapons_model import Weapon
        
        db = self._get_db()
        return db.query(WeaponCategory)\
                 .outerjoin(Weapon, WeaponCategory.id == Weapon.category_id)\
                 .filter(Weapon.id.is_(None))\
                 .all()
    
    def is_name_unique(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Verifica si un nombre de categoría es único.
        
        Args:
            name: Nombre a verificar
            exclude_id: ID a excluir de la verificación (para updates)
            
        Returns:
            bool: True si es único, False si ya existe
            
        Example:
            is_unique = repo.is_name_unique("New Category")
            is_unique_for_update = repo.is_name_unique("Updated Name", exclude_id=1)
        """
        db = self._get_db()
        query = db.query(WeaponCategory).filter(WeaponCategory.name == name)
        
        if exclude_id:
            query = query.filter(WeaponCategory.id != exclude_id)
        
        return query.first() is None
    
    def get_ordered_by_name(self, ascending: bool = True) -> List[WeaponCategory]:
        """
        Obtiene categorías ordenadas por nombre.
        
        Args:
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            List[WeaponCategory]: Categorías ordenadas por nombre
            
        Example:
            categories_asc = repo.get_ordered_by_name(True)
            categories_desc = repo.get_ordered_by_name(False)
        """
        db = self._get_db()
        query = db.query(WeaponCategory)
        
        if ascending:
            return query.order_by(WeaponCategory.name.asc()).all()
        else:
            return query.order_by(WeaponCategory.name.desc()).all()
    
    def create_if_not_exists(self, name: str, description: str = None) -> tuple[WeaponCategory, bool]:
        """
        Crea una categoría solo si no existe una con el mismo nombre.
        
        Args:
            name: Nombre de la categoría
            description: Descripción opcional
            
        Returns:
            tuple[WeaponCategory, bool]: (categoría, fue_creada)
                - categoría: El objeto WeaponCategory
                - fue_creada: True si se creó, False si ya existía
                
        Example:
            category, created = repo.create_if_not_exists("Bow", "Arco tradicional")
            if created:
                print("Categoría creada")
            else:
                print("Categoría ya existía")
        """
        existing = self.find_by_name(name)
        if existing:
            return existing, False
        
        new_category = self.create(name=name, description=description)
        return new_category, True
