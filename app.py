from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Cargar variables de entorno
load_dotenv()

# Inicializar Flask
app = Flask(_name_)

# Permitir solo el dominio específico
CORS(app, resources={
    r"/usuario/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/roles/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/bastones/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/distancia/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"}
})

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "Prueba dia 08-02-2025")

# Inicializar extensiones
db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

# Ruta de prueba
@app.route("/")
def home():
    return "¡Hola, mundo!"

# Importar y registrar Blueprints
from routes.rutas import usuario_bp, roles_bp, baston_bp, distancia_bp

app.register_blueprint(usuario_bp, url_prefix="/usuario")
app.register_blueprint(roles_bp, url_prefix="/roles")
app.register_blueprint(baston_bp, url_prefix="/bastones")
app.register_blueprint(distancia_bp, url_prefix="/distancia")

# Ejecutar la aplicación
if _name_ == "_main_":
    app.run(host="0.0.0.0", port=8000, debug=True)# Escuchar en todas las interfaces