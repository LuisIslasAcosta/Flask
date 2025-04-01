# app.py
from flask import Flask
from config import db, migrate
from dotenv import load_dotenv
from flask import Flask, render_template
import os
from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Permitir solo el dominio específico
CORS(app, resources={
    r"/usuario/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/roles/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/bastones/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"},
    r"/distancia/*": {"origins": "https://main.d3gd2kcl7rhrjn.amplifyapp.com"}
})


# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'Prueba dia 08-02-2025'

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy, Flask-Migrate y JWTManager
db.init_app(app)
migrate.init_app(app, db)
jwt = JWTManager(app)

# Ruta de prueba
@app.route("/")
def home():
    return render_template("index.html")

# Importar los Blueprints de usuarios y roles
from routes.rutas import usuario_bp, roles_bp, baston_bp, distancia_bp

# Registrar los Blueprints
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(roles_bp, url_prefix='/roles')
app.register_blueprint(baston_bp, url_prefix='/bastones')
app.register_blueprint(distancia_bp, url_prefix='/distancia')

# Correr la aplicación
if __name__ == '__main__':
    app.run(debug=True)
