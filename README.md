# Monster Hunter Weapons API

Una API REST desarrollada en Flask para gestionar categorías de armas de Monster Hunter.

## Características

- **CRUD completo** para categorías de armas y armas
- **Base de datos PostgreSQL** en Railway
- **Arquitectura MVC** (Modelo-Vista-Controlador)
- **SQLAlchemy** como ORM
- **Validaciones** de integridad de datos

## Tecnologías

- Python 3.11+
- Flask
- SQLAlchemy
- PostgreSQL
- python-dotenv

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/SeanOsorio/ClassApi.git
   cd ClassApi
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno en `.env`:
   ```env
   DBUSER=tu_usuario
   DBPASSWORD=tu_contraseña
   DBHOST=tu_host
   DBPORT=5432
   DBNAME=tu_base_datos
   ```

5. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Endpoints

### Categorías de Armas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/categories` | Obtener todas las categorías |
| GET | `/categories/{id}` | Obtener categoría por ID |
| POST | `/categories` | Crear nueva categoría |
| PUT | `/categories/{id}` | Actualizar categoría |
| DELETE | `/categories/{id}` | Eliminar categoría |

### Armas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/weapons/{id}` | Obtener arma por ID |
| POST | `/weapons` | Crear nueva arma |
| PUT | `/weapons/{id}` | Actualizar arma |
| DELETE | `/weapons/{id}` | Eliminar arma |

## Ejemplos de Uso

### Crear una categoría
```bash
POST /categories
Content-Type: application/json

{
  "name": "Great Swords",
  "description": "Armas de dos manos con gran alcance"
}
```

### Crear un arma
```bash
POST /weapons
Content-Type: application/json

{
  "name": "Rathalos Glinsword",
  "category_id": 1,
  "description": "Espada forjada con materiales de Rathalos"
}
```

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal
├── config/
│   └── database.py       # Configuración de base de datos
├── controllers/
│   └── weapons_controller.py  # Controladores REST
├── models/
│   └── weapons_model.py      # Modelos SQLAlchemy
├── services/
│   └── weapons_service.py    # Lógica de negocio
└── requirements.txt      # Dependencias
```

## Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.