from models.models import Roles, Usuario, Baston, BastonesUsuario, Ubicacion, ContactoEmergencia, AlertaEmergencia
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token

# Obtener todos los roles - Listo
def get_all_roles():
    try:
        roles = [role.to_dict() for role in Roles.query.all()]
        return jsonify(roles)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener los roles'}), 500

# Crear un nuevo rol - Listo
def create_rol(nombre):
    try:
        new_rol = Roles(nombre)
        db.session.add(new_rol)
        db.session.commit()
        return jsonify(new_rol.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el rol'}), 500

# Obtener un usuario por su ID
def get_usuario_por_id(usuario_id):
    try:
        # Buscar el usuario por su ID
        usuario = Usuario.query.get(usuario_id)
        
        # Si el usuario no existe, devolver un mensaje de error
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        
        # Devolver los datos del usuario encontrado
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener el usuario'}), 500
    
# Editar un usuario
def edit_usuario(usuario_id, nombre=None, email=None, telefono=None, password=None, rol_id=None):
    try:
        # Buscar el usuario por su ID
        usuario = Usuario.query.get(usuario_id)
        
        # Si el usuario no existe, devolver un mensaje de error
        if not usuario:
            return jsonify({'msg': 'Usuario no encontrado'}), 404
        
        # Actualizar los campos solo si se proporcionan nuevos valores
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        if telefono:
            usuario.telefono = telefono
        if password:
            usuario.password = password  # Es recomendable encriptar el password si es necesario
        if rol_id:
            usuario.rol_id = rol_id
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        # Devolver el usuario actualizado
        return jsonify(usuario.to_dict()), 200
        
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al editar el usuario'}), 500

# Obtener todos los usuarios - Listo
def get_all_usuarios():
    try:
        usuarios = [usuario.to_dict() for usuario in Usuario.query.all()]
        return jsonify(usuarios)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener los usuarios'}), 500

# Crear un nuevo usuario - Listo
def create_usuario(nombre, email, telefono, password, rol_id):
    try:
        nuevo_usuario = Usuario(nombre, email, telefono, password, rol_id)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify(nuevo_usuario.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el usuario'}), 500

# Login de usuario
def login_usuario(email, password):
    try:
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(password):
            access_token = create_access_token(identity=usuario.id)
            return jsonify({
                'access_token': access_token,
                'usuario': {
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "telefono": usuario.telefono,
                    "rol_id": usuario.rol_id,
                    "rol_nombre": usuario.rol.nombre  # Aquí pasamos el nombre del rol
                }
            })
        return jsonify({"msg": "Credenciales inválidas"}), 401
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error en el login'}), 500

# Obtener todos los bastones
def get_all_bastones():
    try:
        bastones = [baston.to_dict() for baston in Baston.query.all()]
        return jsonify(bastones)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener los bastones'}), 500

# Crear un nuevo bastón
def create_baston(nombre):
    try:
        new_baston = Baston(nombre)
        db.session.add(new_baston)
        db.session.commit()
        return jsonify(new_baston.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el bastón'}), 500

# Eliminar un bastón
def delete_baston(baston_id):
    try:
        # Buscar el bastón por ID
        baston = Baston.query.get(baston_id)
        if not baston:
            return jsonify({'msg': 'Bastón no encontrado'}), 404

        # Eliminar el bastón de la base de datos
        db.session.delete(baston)
        db.session.commit()
        
        return jsonify({'msg': 'Bastón eliminado exitosamente'}), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al eliminar el bastón'}), 500


# Relacionar bastón con un usuario
def asignar_baston_usuario(usuario_id, baston_id):
    try:
        baston_usuario = BastonesUsuario(usuario_id=usuario_id, baston_id=baston_id)
        db.session.add(baston_usuario)
        db.session.commit()
        return jsonify(baston_usuario.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al asignar el bastón al usuario'}), 500
    
# Obtener todas las asignaciones de bastones a usuarios
def get_all_bastones_usuarios():
    try:
        asignaciones = BastonesUsuario.query.all()
        resultado = [asignacion.to_dict() for asignacion in asignaciones]
        return jsonify(resultado), 200
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al obtener las asignaciones'}), 500


# Obtener todas las ubicaciones
def get_all_ubicaciones():
    try:
        ubicaciones = [ubicacion.to_dict() for ubicacion in Ubicacion.query.all()]
        return jsonify(ubicaciones)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener las ubicaciones'}), 500

# Crear una nueva ubicación
def create_ubicacion(usuario_id, latitud, longitud, direccion=None, baston_id=None):
    try:
        nueva_ubicacion = Ubicacion(usuario_id=usuario_id, latitud=latitud, longitud=longitud, direccion=direccion, baston_id=baston_id)
        db.session.add(nueva_ubicacion)
        db.session.commit()
        return jsonify(nueva_ubicacion.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear la ubicación'}), 500

# Obtener todos los contactos de emergencia
def get_all_contactos_emergencia():
    try:
        contactos = [contacto.to_dict() for contacto in ContactoEmergencia.query.all()]
        return jsonify(contactos)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener los contactos de emergencia'}), 500

# Crear un nuevo contacto de emergencia
def create_contacto_emergencia(usuario_id, nombre, telefono, email=None):
    try:
        nuevo_contacto = ContactoEmergencia(usuario_id=usuario_id, nombre=nombre, telefono=telefono, email=email)
        db.session.add(nuevo_contacto)
        db.session.commit()
        return jsonify(nuevo_contacto.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear el contacto de emergencia'}), 500

# Obtener todas las alertas de emergencia
def get_all_alertas_emergencia():
    try:
        alertas = [alerta.to_dict() for alerta in AlertaEmergencia.query.all()]
        return jsonify(alertas)
    except Exception as error:
        print(f"ERROR {error}")
        return jsonify({'msg': 'Error al obtener las alertas de emergencia'}), 500

# Crear una nueva alerta de emergencia
def create_alerta_emergencia(usuario_id, tipo_alerta, ubicacion_id=None, contacto_id=None, estado='pendiente'):
    try:
        nueva_alerta = AlertaEmergencia(usuario_id=usuario_id, tipo_alerta=tipo_alerta, ubicacion_id=ubicacion_id, contacto_id=contacto_id, estado=estado)
        db.session.add(nueva_alerta)
        db.session.commit()
        return jsonify(nueva_alerta.to_dict()), 201
    except Exception as e:
        print(f"ERROR {e}")
        return jsonify({'msg': 'Error al crear la alerta de emergencia'}), 500
