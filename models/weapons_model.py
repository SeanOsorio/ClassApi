
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Modelo para categorías de armas
class WeaponCategory(Base):
	__tablename__ = 'weapon_categories'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False, unique=True)
	description = Column(String(255), nullable=True)

# Modelo para armas
class Weapon(Base):
	__tablename__ = 'weapons'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(100), nullable=False)
	category_id = Column(Integer, ForeignKey('weapon_categories.id'))
	description = Column(String(255), nullable=True)
