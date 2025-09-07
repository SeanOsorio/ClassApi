
"""
Monster Hunter Weapons API - Aplicación Principal

Esta es la API REST completa para gestionar categorías de armas y armas específicas
del universo Monster Hunter. Proporciona endpoints para operaciones CRUD completas
con validaciones, manejo de errores y arquitectura MVC.

Características principales:
- ✅ CRUD completo para categorías y armas
- ✅ Base de datos PostgreSQL en Railway
- ✅ Validaciones de integridad referencial
- ✅ IDs independientes por tabla
- ✅ Manejo robusto de errores HTTP
- ✅ Documentación completa de endpoints

Autor: Sean Osorio
Repositorio: https://github.com/SeanOsorio/ClassApi
Licencia: MIT
"""

from flask import Flask, jsonify
from controllers.weapons_controller import weapons_bp
from config.database import init_db

# =============================================================================
# INICIALIZACIÓN DE LA APLICACIÓN FLASK
# =============================================================================

def create_app():
    """
    Factory function para crear y configurar la aplicación Flask.
    
    Esta función encapsula la creación de la app y permite:
    - Testing más fácil
    - Múltiples configuraciones (dev, prod, test)
    - Inicialización controlada de componentes
    
    Returns:
        Flask: Aplicación Flask configurada y lista para usar
    """
    # Crear instancia de Flask
    app = Flask(__name__)
    
    # Configuraciones básicas
    app.config['JSON_SORT_KEYS'] = False  # Preservar orden en respuestas JSON
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # JSON formateado en desarrollo
    
    return app

# Crear la aplicación principal
app = create_app()

# =============================================================================
# INICIALIZACIÓN DE BASE DE DATOS
# =============================================================================

print("🚀 Iniciando Monster Hunter Weapons API...")
print("🔗 Conectando a base de datos PostgreSQL...")

# Inicializar base de datos al arrancar la aplicación
# Esto crea las tablas si no existen (safe operation)
init_db()

print("📊 Base de datos inicializada correctamente")

# =============================================================================
# REGISTRO DE BLUEPRINTS (RUTAS)
# =============================================================================

# Registrar blueprint de armas y categorías
# Esto incluye todos los endpoints definidos en weapons_controller.py
app.register_blueprint(weapons_bp)

print("🛣️  Rutas registradas:")
print("   • GET    /categories              - Listar categorías")
print("   • POST   /categories              - Crear categoría")  
print("   • GET    /categories/{id}         - Obtener categoría")
print("   • PUT    /categories/{id}         - Actualizar categoría")
print("   • DELETE /categories/{id}         - Eliminar categoría")
print("   • GET    /categories/{id}/weapons - Armas por categoría")
print("   • GET    /weapons                 - Listar armas")
print("   • POST   /weapons                 - Crear arma")
print("   • GET    /weapons/{id}            - Obtener arma")
print("   • PUT    /weapons/{id}            - Actualizar arma")
print("   • DELETE /weapons/{id}            - Eliminar arma")

# =============================================================================
# ENDPOINTS ADICIONALES
# =============================================================================

@app.route('/')
def home():
    """
    Endpoint raíz que proporciona información básica de la API.
    
    Returns:
        JSON: Información de bienvenida y enlaces útiles
    """
    return jsonify({
        'message': '🏹 Monster Hunter Weapons API',
        'version': '1.0.0',
        'description': 'API REST para gestión de categorías y armas de Monster Hunter',
        'endpoints': {
            'categories': '/categories',
            'weapons': '/weapons',
            'documentation': 'https://github.com/SeanOsorio/ClassApi'
        },
        'status': 'online',
        'author': 'Sean Osorio'
    })

@app.route('/health')
def health_check():
    """
    Endpoint de health check para monitoreo.
    
    Returns:
        JSON: Estado de salud de la aplicación y base de datos
    """
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'api_version': '1.0.0'
    })

# =============================================================================
# MANEJO GLOBAL DE ERRORES
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    """Manejador para errores 404 - Recurso no encontrado."""
    return jsonify({
        'error': 'Endpoint no encontrado',
        'message': 'Verifica la URL y el método HTTP',
        'available_endpoints': [
            'GET /categories',
            'POST /categories', 
            'GET /weapons',
            'POST /weapons'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejador para errores 405 - Método no permitido."""
    return jsonify({
        'error': 'Método HTTP no permitido',
        'message': 'Verifica que estés usando el método correcto (GET, POST, PUT, DELETE)'
    }), 405

@app.errorhandler(500)
def internal_server_error(error):
    """Manejador para errores 500 - Error interno del servidor."""
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ha ocurrido un error inesperado. Inténtalo más tarde.'
    }), 500

# =============================================================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# =============================================================================

if __name__ == '__main__':
    print("=" * 50)
    print("🎮 MONSTER HUNTER WEAPONS API")
    print("=" * 50)
    print("🌐 Servidor iniciando en: http://127.0.0.1:5000")
    print("📚 Documentación: https://github.com/SeanOsorio/ClassApi")
    print("🐛 Modo debug: ACTIVADO")
    print("=" * 50)
    
    # Iniciar servidor Flask en modo desarrollo
    app.run(
        debug=True,        # Modo debug para desarrollo
        host='127.0.0.1',  # Solo accesible localmente
        port=5000          # Puerto estándar para desarrollo
    )
