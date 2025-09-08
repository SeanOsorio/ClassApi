"""
Repository para el manejo de armas específicas.

Este módulo contiene toda la lógica de acceso a datos específica
para la entidad Weapon, incluyendo operaciones CRUD y consultas
especializadas relacionadas con armas y sus categorías.
"""

from typing import List, Optional
from sqlalchemy import and_, or_
from models.weapons_model import Weapon, WeaponCategory
from repository.base_repository import BaseRepository


class WeaponRepository(BaseRepository[Weapon]):
    """
    Repository específico para armas.
    
    Hereda operaciones CRUD básicas de BaseRepository y añade
    funcionalidades específicas para armas y sus relaciones con categorías.
    """
    
    def __init__(self):
        """Inicializa el repository con el modelo Weapon."""
        super().__init__(Weapon)
    
    def find_by_category_id(self, category_id: int) -> List[Weapon]:
        """
        Obtiene todas las armas de una categoría específica.
        
        Args:
            category_id: ID de la categoría de armas
            
        Returns:
            List[Weapon]: Lista de armas de la categoría
            
        Example:
            great_swords = repo.find_by_category_id(1)
        """
        db = self._get_db()
        return db.query(Weapon).filter(
            Weapon.category_id == category_id
        ).all()
    
    def find_by_name(self, name: str) -> Optional[Weapon]:
        """
        Busca un arma por su nombre exacto.
        
        Args:
            name: Nombre del arma a buscar
            
        Returns:
            Optional[Weapon]: Arma si existe, None si no se encuentra
            
        Example:
            weapon = repo.find_by_name("Rathalos Glinsword")
        """
        db = self._get_db()
        return db.query(Weapon).filter(
            Weapon.name == name
        ).first()
    
    def search_by_name_pattern(self, pattern: str) -> List[Weapon]:
        """
        Busca armas por patrón de nombre (case-insensitive).
        
        Args:
            pattern: Patrón de búsqueda (ej: "%rathalos%")
            
        Returns:
            List[Weapon]: Lista de armas que coinciden con el patrón
            
        Example:
            rathalos_weapons = repo.search_by_name_pattern("%rathalos%")
        """
        db = self._get_db()
        return db.query(Weapon).filter(
            Weapon.name.ilike(pattern)
        ).all()
    
    def search_by_description(self, keyword: str) -> List[Weapon]:
        """
        Busca armas por palabra clave en la descripción.
        
        Args:
            keyword: Palabra clave a buscar
            
        Returns:
            List[Weapon]: Armas con la palabra en descripción
            
        Example:
            fire_weapons = repo.search_by_description("fuego")
        """
        db = self._get_db()
        return db.query(Weapon).filter(
            Weapon.description.ilike(f"%{keyword}%")
        ).all()
    
    def get_weapons_with_category_info(self) -> List[tuple]:
        """
        Obtiene armas con información completa de su categoría.
        
        Returns:
            List[tuple]: Lista de (Weapon, WeaponCategory) tuplas
            
        Example:
            for weapon, category in repo.get_weapons_with_category_info():
                print(f"{weapon.name} - {category.name}")
        """
        db = self._get_db()
        return db.query(Weapon, WeaponCategory)\
                 .join(WeaponCategory, Weapon.category_id == WeaponCategory.id)\
                 .all()
    
    def get_weapons_by_category_name(self, category_name: str) -> List[Weapon]:
        """
        Obtiene armas por el nombre de la categoría.
        
        Args:
            category_name: Nombre de la categoría
            
        Returns:
            List[Weapon]: Armas de la categoría especificada
            
        Example:
            dual_blades = repo.get_weapons_by_category_name("Dual Blades")
        """
        db = self._get_db()
        return db.query(Weapon)\
                 .join(WeaponCategory, Weapon.category_id == WeaponCategory.id)\
                 .filter(WeaponCategory.name == category_name)\
                 .all()
    
    def count_by_category(self, category_id: int) -> int:
        """
        Cuenta las armas en una categoría específica.
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            int: Número de armas en la categoría
            
        Example:
            count = repo.count_by_category(1)
        """
        db = self._get_db()
        return db.query(Weapon).filter(
            Weapon.category_id == category_id
        ).count()
    
    def get_ordered_by_name(self, category_id: Optional[int] = None, ascending: bool = True) -> List[Weapon]:
        """
        Obtiene armas ordenadas por nombre, opcionalmente filtradas por categoría.
        
        Args:
            category_id: ID de categoría para filtrar (opcional)
            ascending: True para orden ascendente, False para descendente
            
        Returns:
            List[Weapon]: Armas ordenadas por nombre
            
        Example:
            all_weapons_asc = repo.get_ordered_by_name()
            great_swords_desc = repo.get_ordered_by_name(category_id=1, ascending=False)
        """
        db = self._get_db()
        query = db.query(Weapon)
        
        if category_id:
            query = query.filter(Weapon.category_id == category_id)
        
        if ascending:
            return query.order_by(Weapon.name.asc()).all()
        else:
            return query.order_by(Weapon.name.desc()).all()
    
    def search_weapons_advanced(
        self,
        name_pattern: Optional[str] = None,
        description_keyword: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None
    ) -> List[Weapon]:
        """
        Búsqueda avanzada de armas con múltiples criterios.
        
        Args:
            name_pattern: Patrón para nombre de arma
            description_keyword: Palabra clave en descripción
            category_id: ID de categoría específica
            category_name: Nombre de categoría específica
            
        Returns:
            List[Weapon]: Armas que coinciden con los criterios
            
        Example:
            weapons = repo.search_weapons_advanced(
                name_pattern="%sword%",
                category_name="Great Sword"
            )
        """
        db = self._get_db()
        query = db.query(Weapon)
        
        # Join con categoría si se necesita buscar por nombre de categoría
        if category_name:
            query = query.join(WeaponCategory, Weapon.category_id == WeaponCategory.id)
        
        # Aplicar filtros según parámetros proporcionados
        filters = []
        
        if name_pattern:
            filters.append(Weapon.name.ilike(name_pattern))
        
        if description_keyword:
            filters.append(Weapon.description.ilike(f"%{description_keyword}%"))
        
        if category_id:
            filters.append(Weapon.category_id == category_id)
        
        if category_name:
            filters.append(WeaponCategory.name == category_name)
        
        # Aplicar todos los filtros con AND
        if filters:
            query = query.filter(and_(*filters))
        
        return query.all()
    
    def create_with_category_validation(self, name: str, category_id: int, description: str = None) -> Optional[Weapon]:
        """
        Crea un arma validando que la categoría existe.
        
        Args:
            name: Nombre del arma
            category_id: ID de la categoría
            description: Descripción opcional
            
        Returns:
            Optional[Weapon]: Arma creada o None si la categoría no existe
            
        Example:
            weapon = repo.create_with_category_validation(
                "New Sword", 1, "A powerful sword"
            )
        """
        db = self._get_db()
        
        # Verificar que la categoría existe
        category_exists = db.query(WeaponCategory).filter(
            WeaponCategory.id == category_id
        ).first() is not None
        
        if not category_exists:
            return None
        
        # Crear el arma si la categoría es válida
        return self.create(
            name=name,
            category_id=category_id,
            description=description
        )
    
    def delete_all_from_category(self, category_id: int) -> int:
        """
        Elimina todas las armas de una categoría específica.
        
        CUIDADO: Esta operación elimina múltiples registros.
        
        Args:
            category_id: ID de la categoría
            
        Returns:
            int: Número de armas eliminadas
            
        Example:
            deleted_count = repo.delete_all_from_category(1)
            print(f"Eliminadas {deleted_count} armas")
        """
        db = self._get_db()
        weapons_to_delete = db.query(Weapon).filter(
            Weapon.category_id == category_id
        )
        
        count = weapons_to_delete.count()
        weapons_to_delete.delete()
        db.commit()
        
        return count
