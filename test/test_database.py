import os
import psycopg2
from dotenv import load_dotenv

def test_database_connection():
    """
    Prueba la conexión a la base de datos PostgreSQL usando variables del archivo .env
    """
    # Cargar variables del archivo .env
    load_dotenv()
    
    # Obtener las variables de entorno
    username = os.getenv('DBUSER')
    password = os.getenv('DBPASSWORD')
    host = os.getenv('DBHOST')
    port = os.getenv('DBPORT')
    database = os.getenv('DBNAME')

    print("Intentando conectar a la base de datos...")
    print(f"Host: {host}")
    print(f"Puerto: {port}")
    print(f"Base de datos: {database}")
    print(f"Usuario: {username}")
    print(f"Contraseña: {password}")

    try:
        # Crear la conexión
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password
        )
        
        # Crear un cursor para ejecutar consultas
        cursor = connection.cursor()
        
        # Ejecutar una consulta simple para verificar la conexión
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        
        print("✅ ¡Conexión exitosa!")
        print(f"Versión de PostgreSQL: {db_version[0]}")
        
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        
        return True
        
    except psycopg2.Error as e:
        print("❌ Error al conectar a la base de datos:")
        print(f"Código de error: {e.pgcode}")
        print(f"Mensaje: {e.pgerror}")
        return False
        
    except Exception as e:
        print("❌ Error inesperado:")
        print(f"Mensaje: {str(e)}")
        return False

if __name__ == "__main__":
    test_database_connection()