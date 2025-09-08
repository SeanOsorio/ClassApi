"""
Configuración de base de datos para la API de Monster Hunter Weapons.

Este módulo maneja:
- Conexión a PostgreSQL en Railway usando variables de entorno
- Creación del motor SQLAlchemy con configuraciones optimizadas
- Gestión de sesiones de base de datos con context manager
- Inicialización automática de tablas

Variables de entorno requeridas:
- DBUSER: Usuario de la base de datos
- DBPASSWORD: Contraseña del usuario
- DBHOST: Host del servidor PostgreSQL
- DBPORT: Puerto (por defecto 5432)
- DBNAME: Nombre de la base de datos
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.weapons_model import Base
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
load_dotenv()

# =============================================================================
# CONFIGURACIÓN DE VARIABLES DE ENTORNO
# =============================================================================

# Obtener credenciales de base de datos desde variables de entorno
# Estas variables deben estar definidas en el archivo .env
DBUSER = os.getenv('DBUSER')
DBPASSWORD = os.getenv('DBPASSWORD') 
DBHOST = os.getenv('DBHOST')
DBPORT = os.getenv('DBPORT', '5432')  # Puerto por defecto para PostgreSQL
DBNAME = os.getenv('DBNAME')

# Validar que todas las variables requeridas estén presentes
required_vars = ['DBUSER', 'DBPASSWORD', 'DBHOST', 'DBNAME']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise ValueError(f"Variables de entorno faltantes: {', '.join(missing_vars)}")

# =============================================================================
# CONFIGURACIÓN DE CONEXIÓN A BASE DE DATOS
# =============================================================================

# Construir URL de conexión para PostgreSQL
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
DATABASE_URL = f"postgresql://{DBUSER}:{DBPASSWORD}@{DBHOST}:{DBPORT}/{DBNAME}"

# Crear motor SQLAlchemy con configuraciones para producción
engine = create_engine(
    DATABASE_URL, 
    echo=False,  # Ocultar SQL queries para producción limpia
    pool_pre_ping=True,  # Verificar conexiones antes de usarlas
    pool_recycle=3600,   # Reciclar conexiones cada hora
    max_overflow=20,     # Máximo de conexiones adicionales en pool
    pool_size=10         # Tamaño base del pool de conexiones
)

# Configurar factory de sesiones
SessionLocal = sessionmaker(
    autocommit=False,    # No autocommit - control manual de transacciones
    autoflush=False,     # No autoflush - control manual del flushing  
    bind=engine          # Motor de base de datos asociado
)


# =============================================================================
# GESTIÓN DE SESIONES DE BASE DE DATOS
# =============================================================================

def get_db():
    """
    Generador de sesiones de base de datos con context manager.
    
    Este generador asegura que:
    - La sesión se cierre automáticamente al finalizar
    - Los recursos se liberen correctamente
    - No haya memory leaks por conexiones abiertas
    
    Usage:
        db = next(get_db())  # En servicios
        # O usando yield from en dependencias
        
    Yields:
        Session: Sesión SQLAlchemy lista para usar
        
    Example:
        def get_all_weapons():
            db = next(get_db())
            return db.query(Weapon).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        # Asegurar que la sesión se cierre correctamente
        db.close()


# =============================================================================
# INICIALIZACIÓN DE BASE DE DATOS
# =============================================================================

def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas.
    
    Esta función:
    - Lee todos los modelos definidos en models/
    - Crea las tablas que no existan
    - Configura claves foráneas y constraints
    - Es segura para ejecutar múltiples veces (CREATE IF NOT EXISTS)
    
    Debe ejecutarse:
    - Al iniciar la aplicación por primera vez
    - Después de cambios en los modelos
    - En el deployment a producción
    
    Tables created:
        - weapon_categories: Categorías de armas (Great Sword, etc.)
        - weapons: Armas específicas con referencia a categorías
        
    Example:
        # En app.py al iniciar la aplicación
        init_db()
        print("Base de datos inicializada correctamente")
    """
    print("🔄 Inicializando base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas/verificadas correctamente")