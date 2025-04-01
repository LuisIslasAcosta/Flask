from flask import Blueprint, jsonify, request
from controllers.controllers import get_all_roles, create_rol, create_usuario, get_all_bastones, create_baston
from controllers.controllers import edit_usuario, get_usuario_por_id, delete_baston, create_access_token
from models.models import Usuario

# Blueprints
usuario_bp = Blueprint('usuarios', __name__)
roles_bp = Blueprint('roles', __name__)
baston_bp = Blueprint('bastones', __name__)

# ------------------------------------- Roles -------------------------------------- #

# Ruta para obtener todos los roles
@roles_bp.route('/roles', methods=['GET'])
def obtener_roles():
    return get_all_roles()

# Ruta para crear un nuevo rol
@roles_bp.route('/', methods=['POST'])
def create_rol_route():
    data = request.get_json()
    nombre = data.get('nombre')
    
    if not nombre:
        return jsonify({"error": "Faltan campos requeridos"}), 400
    
    return create_rol(nombre)

# -------------------------------------- Usuarios y Registros --------------------------- #
# Ruta para crear un nuevo usuario
@usuario_bp.route('/', methods=['POST'], strict_slashes=False)

def usuario_store():
    data = request.get_json()
    email = data.get('email')
    nombre = data.get('nombre')
    password = data.get('password')
    telefono = data.get('telefono')

    # Asignar rol_id por defecto si no se recibe
    rol_id = data.get('rol_id', 1)  # Asignar rol_id 1 por defecto (usuario regular)

    # Validar que todos los campos necesarios estén presentes
    if not all([email, nombre, password, telefono]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Llamar a la función para crear el usuario
    return create_usuario(nombre, email, telefono, password, rol_id)

# Ruta para login de usuario con token JWT
@usuario_bp.route('/login', methods=['POST'])
def login_usuario_route():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validar que los campos no estén vacíos
    if not email or not password:
        return jsonify({"error": "Email y contraseña son requeridos"}), 400

    try:
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            # Aquí generamos el token JWT
            access_token = create_access_token(identity=usuario.id)

            # Retornamos la respuesta con los datos del usuario, incluido el rol
            return jsonify({
                "message": "Login exitoso",
                "access_token": access_token,
                "usuario": {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "telefono": usuario.telefono,
                    "rol_id": usuario.rol_id,
                    "rol_nombre": usuario.rol.nombre  # Aquí incluimos el nombre del rol
                }
            }), 200

        else:
            return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Login fallido"}), 500
    
# Ruta para obtener todos los usuarios
@usuario_bp.route('/obtener', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify([usuario.to_dict() for usuario in usuarios]), 200
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Error al obtener los usuarios"}), 500


# Ruta para obtener perfil de usuario
@usuario_bp.route('/perfil', methods=['GET'])
def obtener_perfil():
    email = request.args.get('email')  # Obtener el email desde la query string
    if not email:
        return jsonify({"error": "Email requerido"}), 400

    try:
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            return jsonify(usuario.to_dict()), 200
        return jsonify({"error": "Usuario no encontrado"}), 404
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": "Error al obtener el perfil"}), 500

# Ruta para editar un usuario
@usuario_bp.route('/<int:usuario_id>', methods=['PUT'])
def editar_usuario(usuario_id):
    data = request.get_json()
    
    # Obtener los valores desde el JSON (todos son opcionales)
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono')
    password = data.get('password')
    rol_id = data.get('rol_id')

    # Llamamos a la función edit_usuario con los datos proporcionados
    return edit_usuario(usuario_id, nombre, email, telefono, password, rol_id)

# Ruta para obtener un usuario por ID
@usuario_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    return get_usuario_por_id(id)

# ---------------------------------------- Bastones -------------------------------- #

# Ruta para crear un nuevo bastón
@baston_bp.route('/create_baston', methods=['POST'])
def create_baston_route():
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'msg': 'El nombre es obligatorio'}), 400

    # Llamamos a la función del controlador
    return create_baston(nombre)

# Ruta para obtener todos los bastones
@baston_bp.route('/bastones', methods=['GET'])
def get_all_bastones_route():
    return get_all_bastones()

# Ruta para eliminar un bastón
@baston_bp.route('/<int:baston_id>', methods=['DELETE'])
def eliminar_baston(baston_id):
    return delete_baston(baston_id)


#--------------------------------- Distancia --------------------------------#
from flask import Blueprint, request, jsonify

distancia_bp = Blueprint("distancia", __name__)

datos_sensores = {"distancia": 0, "ir1": 0, "ir2": 0}

@distancia_bp.route("/", methods=["POST"], strict_slashes=False)
def recibir_datos():
    global datos_sensores
    data = request.get_json()

    if data and "distancia" in data and "ir1" in data and "ir2" in data:
        datos_sensores["distancia"] = data["distancia"]
        datos_sensores["ir1"] = data["ir1"]
        datos_sensores["ir2"] = data["ir2"]

        print(f"Datos recibidos -> Distancia: {data['distancia']} cm, IR1: {data['ir1']}, IR2: {data['ir2']}")
        return jsonify({"mensaje": "Datos recibidos correctamente", "datos": datos_sensores}), 200
    else:
        return jsonify({"mensaje": "Error en los datos recibidos"}), 400

@distancia_bp.route("/", methods=["GET"], strict_slashes=False)
def obtener_datos():
    return jsonify(datos_sensores), 200