import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.weapons_model import Base
from dotenv import load_dotenv

load_dotenv()

# Obtener los parámetros individuales de la base de datos

DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD')
DBHOST = os.getenv('DBHOST')
DBPORT = os.getenv('DBPORT', '5432')
DBNAME = os.getenv('DBNAME')

# Construir la URL de conexión para PostgreSQL
DATABASE_URL = f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

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