from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from decimal import Decimal

# Modelo de Roles
class Roles(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    
    def __init__(self, nombre):
        self.nombre = nombre
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relación entre Usuario y Roles
    rol = db.relationship('Roles', backref='usuarios', lazy=True)

    def __init__(self, nombre, email, telefono, password, rol_id):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.password = generate_password_hash(password)
        self.rol_id = rol_id

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
            "rol_id": self.rol_id,
            "rol_nombre": self.rol.nombre  # Agregar nombre del rol al diccionario
        }

# Modelo de Bastón
class Baston(db.Model):
    __tablename__ = 'bastones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relación con la tabla bastones_usuarios
    usuarios = db.relationship('BastonesUsuario', backref='baston', lazy=True)

    def __init__(self, nombre):
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre
        }

# Modelo de BastonesUsuarios (relación entre Bastones y Usuarios)
class BastonesUsuario(db.Model):
    __tablename__ = 'bastones_usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    baston_id = db.Column(db.Integer, db.ForeignKey('bastones.id'), nullable=False)
    fecha_asignacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, usuario_id, baston_id):
        self.usuario_id = usuario_id
        self.baston_id = baston_id

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "baston_id": self.baston_id,
            "fecha_asignacion": self.fecha_asignacion.isoformat() if self.fecha_asignacion else None
        }


# Modelo de Ubicación
class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    baston_id = db.Column(db.Integer, db.ForeignKey('bastones.id'), nullable=True)
    latitud = db.Column(db.Numeric(10, 8), nullable=False)  # Utiliza db.Numeric en lugar de db.Decimal
    longitud = db.Column(db.Numeric(11, 8), nullable=False) # Utiliza db.Numeric en lugar de db.Decimal
    direccion = db.Column(db.String(255), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relaciones
    usuario = db.relationship('Usuario', backref='ubicaciones', lazy=True)
    baston = db.relationship('Baston', backref='ubicaciones', lazy=True)

    def __init__(self, usuario_id, latitud, longitud, direccion=None, baston_id=None):
        self.usuario_id = usuario_id
        self.latitud = latitud
        self.longitud = longitud
        self.direccion = direccion
        self.baston_id = baston_id

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "latitud": str(self.latitud),  # Convertir a string para mayor precisión al devolver
            "longitud": str(self.longitud),  # Convertir a string para mayor precisión
            "direccion": self.direccion,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None
        }
        
        
# Modelo de Contactos de Emergencia
class ContactoEmergencia(db.Model):
    __tablename__ = 'contactos_emergencia'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))

    # Relación con la tabla Usuario
    usuario = db.relationship('Usuario', backref='contactos_emergencia', lazy=True)

    def __init__(self, usuario_id, nombre, telefono, email=None):
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email
        }

# Modelo de Alertas de Emergencia
class AlertaEmergencia(db.Model):
    __tablename__ = 'alertas_emergencia'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_alerta = db.Column(db.Enum('caída', 'zona de riesgo', name='tipo_alerta'), nullable=False)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'), nullable=True)
    contacto_id = db.Column(db.Integer, db.ForeignKey('contactos_emergencia.id'), nullable=True)
    estado = db.Column(db.Enum('pendiente', 'atendida', name='estado_alerta'), default='pendiente', nullable=False)
    fecha_alerta = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relación con las tablas de Usuario, Ubicación y Contacto de Emergencia
    usuario = db.relationship('Usuario', backref='alertas_emergencia', lazy=True)
    ubicacion = db.relationship('Ubicacion', backref='alertas_emergencia', lazy=True)
    contacto = db.relationship('ContactoEmergencia', backref='alertas_emergencia', lazy=True)

    def __init__(self, usuario_id, tipo_alerta, ubicacion_id=None, contacto_id=None, estado='pendiente'):
        self.usuario_id = usuario_id
        self.tipo_alerta = tipo_alerta
        self.ubicacion_id = ubicacion_id
        self.contacto_id = contacto_id
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "tipo_alerta": self.tipo_alerta,
            "ubicacion_id": self.ubicacion_id,
            "contacto_id": self.contacto_id,
            "estado": self.estado,
            "fecha_alerta": self.fecha_alerta.isoformat() if self.fecha_alerta else None
        }
