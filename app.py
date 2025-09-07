
from flask import Flask
from controllers.weapons_controller import weapons_bp
from config.database import init_db

# Inicializar la app Flask
app = Flask(__name__)

# Inicializar la base de datos
init_db()

# Registrar el blueprint de armas y categorías
app.register_blueprint(weapons_bp)

if __name__ == '__main__':
	app.run(debug=True)
