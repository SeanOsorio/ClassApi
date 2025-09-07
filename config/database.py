

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.weapons_model import Base
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

def init_db():
	Base.metadata.create_all(bind=engine)
