
"""
Modelos de base de datos para la API de armas de Monster Hunter.

Este módulo define las entidades principales del sistema:
- WeaponCategory: Categorías de armas (Great Sword, Long Sword, etc.)
- Weapon: Armas específicas dentro de cada categoría

Las tablas utilizan auto-incremento estándar de PostgreSQL para IDs únicos
e independientes por tabla, evitando conflictos entre categorías y armas.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

# Base declarativa para todos los modelos SQLAlchemy
Base = declarative_base()


class WeaponCategory(Base):
    """
    Modelo para categorías de armas de Monster Hunter.
    
    Representa los diferentes tipos de armas disponibles como Great Sword,
    Dual Blades, Hammer, etc. Cada categoría puede tener múltiples armas asociadas.
    
    Attributes:
        id (int): Identificador único auto-incrementable
        name (str): Nombre de la categoría (ej: "Great Sword", "Dual Blades")
        description (str): Descripción detallada de la categoría
        weapons (relationship): Relación uno-a-muchos con la tabla de armas
    """
    __tablename__ = 'weapon_categories'
    
    # ID único con auto-incremento independiente
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Nombre de la categoría - requerido y único
    name = Column(String(100), nullable=False, unique=True)
    
    # Descripción opcional de la categoría
    description = Column(String(255), nullable=True)


class Weapon(Base):
    """
    Modelo para armas específicas de Monster Hunter.
    
    Representa armas individuales dentro de cada categoría, como "Rathalos Glinsword"
    en la categoría "Great Sword" o "Fire and Ice" en "Dual Blades".
    
    Attributes:
        id (int): Identificador único auto-incrementable independiente de categorías
        name (str): Nombre específico del arma
        description (str): Descripción detallada del arma y sus características
        category_id (int): Clave foránea que referencia a WeaponCategory
    
    Relationships:
        - Cada arma pertenece a una categoría (many-to-one)
        - Las categorías pueden tener múltiples armas (one-to-many)
    """
    __tablename__ = 'weapons'
    
    # ID único con auto-incremento independiente de weapon_categories
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Nombre del arma específica - requerido
    name = Column(String(100), nullable=False)
    
    # Clave foránea hacia la tabla de categorías - requerido
    # Establece la relación many-to-one (muchas armas -> una categoría)
    category_id = Column(Integer, ForeignKey('weapon_categories.id'))
    
    # Descripción opcional del arma
    description = Column(String(255), nullable=True)