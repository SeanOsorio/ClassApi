
from config.database import get_db
from models.weapons_model import Weapon, WeaponCategory

def get_weapon_by_id(weapon_id):
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    return weapon

# CRUD para armas
def get_all_weapons():
    db = next(get_db())
    return db.query(Weapon).all()

def get_weapons_by_category(category_id):
    db = next(get_db())
    return db.query(Weapon).filter(Weapon.category_id == category_id).all()

# CRUD para categorías de armas
def get_all_categories():
    db = next(get_db())
    return db.query(WeaponCategory).all()

def get_category_by_id(category_id):
    db = next(get_db())
    return db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()

def create_category(data):
    db = next(get_db())
    new_category = WeaponCategory(**data)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def update_category(category_id, new_data):
    db = next(get_db())
    category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
    if category:
        for key, value in new_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_category(category_id):
    db = next(get_db())
    category = db.query(WeaponCategory).filter(WeaponCategory.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category

def create_weapon(data):
    db = next(get_db())
    new_weapon = Weapon(**data)
    db.add(new_weapon)
    db.commit()
    db.refresh(new_weapon)
    return new_weapon

def update_weapon(weapon_id, new_data):
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        for key, value in new_data.items():
            setattr(weapon, key, value)
        db.commit()
        db.refresh(weapon)
    return weapon

def delete_weapon(weapon_id):
    db = next(get_db())
    weapon = db.query(Weapon).filter(Weapon.id == weapon_id).first()
    if weapon:
        db.delete(weapon)
        db.commit()
    return weapon