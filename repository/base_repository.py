"""
Base Repository con operaciones CRUD genéricas.

Este módulo define la clase base que contiene operaciones comunes
de acceso a datos que pueden ser heredadas por repositories específicos.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from sqlalchemy.orm import Session
from config.database import get_db

# Type variable para el modelo genérico
ModelType = TypeVar('ModelType')


class BaseRepository(Generic[ModelType], ABC):
    """
    Repository base con operaciones CRUD genéricas.
    
    Esta clase abstracta define la interfaz común para todos los repositories
    y proporciona implementaciones base para operaciones estándar.
    
    Type Parameters:
        ModelType: El modelo SQLAlchemy que maneja este repository
    """
    
    def __init__(self, model: type[ModelType]):
        """
        Inicializa el repository con el modelo específico.
        
        Args:
            model: Clase del modelo SQLAlchemy
        """
        self.model = model
    
    def _get_db(self) -> Session:
        """
        Obtiene una sesión de base de datos.
        
        Returns:
            Session: Sesión SQLAlchemy activa
        """
        return next(get_db())
    
    def get_all(self) -> List[ModelType]:
        """
        Obtiene todos los registros del modelo.
        
        Returns:
            List[ModelType]: Lista de todos los objetos del modelo
        """
        db = self._get_db()
        return db.query(self.model).all()
    
    def get_by_id(self, entity_id: int) -> Optional[ModelType]:
        """
        Obtiene un registro por su ID.
        
        Args:
            entity_id: ID único del registro
            
        Returns:
            Optional[ModelType]: Objeto si existe, None si no se encuentra
        """
        db = self._get_db()
        return db.query(self.model).filter(self.model.id == entity_id).first()
    
    def create(self, **kwargs) -> ModelType:
        """
        Crea un nuevo registro.
        
        Args:
            **kwargs: Campos del nuevo registro
            
        Returns:
            ModelType: Objeto creado con ID asignado
        """
        db = self._get_db()
        entity = self.model(**kwargs)
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity
    
    def update(self, entity_id: int, **kwargs) -> Optional[ModelType]:
        """
        Actualiza un registro existente.
        
        Args:
            entity_id: ID del registro a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            Optional[ModelType]: Objeto actualizado o None si no existe
        """
        db = self._get_db()
        entity = db.query(self.model).filter(self.model.id == entity_id).first()
        
        if entity:
            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
            db.commit()
            db.refresh(entity)
        
        return entity
    
    def delete(self, entity_id: int) -> Optional[ModelType]:
        """
        Elimina un registro.
        
        Args:
            entity_id: ID del registro a eliminar
            
        Returns:
            Optional[ModelType]: Objeto eliminado o None si no existía
        """
        db = self._get_db()
        entity = db.query(self.model).filter(self.model.id == entity_id).first()
        
        if entity:
            db.delete(entity)
            db.commit()
        
        return entity
    
    def exists(self, entity_id: int) -> bool:
        """
        Verifica si existe un registro con el ID dado.
        
        Args:
            entity_id: ID a verificar
            
        Returns:
            bool: True si existe, False si no
        """
        db = self._get_db()
        return db.query(self.model).filter(self.model.id == entity_id).first() is not None
    
    def count(self) -> int:
        """
        Cuenta el total de registros en la tabla.
        
        Returns:
            int: Número total de registros
        """
        db = self._get_db()
        return db.query(self.model).count()
