from app.models import Usuario
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

def get_all_users():
    """
    Retorna todos los usuarios registrados.
    """
    usuarios = Usuario.query.all()
    list_usuario = [{
        "usuario_id": usuario.usuario_id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "email": usuario.email,
        "baja": usuario.baja,
        "rol": usuario.rol
    } for usuario in usuarios]
    return {'success': True, 'data': list_usuario}, 200

def get_data_usuario(usuario_id):
    """
    Retorna los datos de un usuario por su ID.
    """
    data_usuario = db.session.get(Usuario, usuario_id)
    if not data_usuario:
        return {
            "message": "Usuario no encontrado"
        }, 500
    return {
        "nombre": data_usuario.nombre,
        "apellido": data_usuario.apellido,
        "email": data_usuario.email,
        "usuario_id": data_usuario.usuario_id,
        "rol": data_usuario.rol
    }, 200

def registrar_usuario(data):
    """
    Registra un nuevo usuario si el email no existe.
    """
    usuario_existente = Usuario.query.filter_by(email=data['email']).first()
    if usuario_existente:
        return {
            "mensaje": "El usuario ya existe"
        }, 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=8)
    nuevo_usuario = Usuario(
        rol='usuario', 
        nombre=data['nombre'],
        apellido=data['apellido'],
        email=data['email'],
        password=hashed_password,
        baja=False,
    )
    db.session.add(nuevo_usuario)
    db.session.commit()

    return {
        "mensaje": "Usuario registrado con éxito",
        "usuario": {
            "nombre": nuevo_usuario.nombre,
            "apellido": nuevo_usuario.apellido,
            "email": nuevo_usuario.email,
            "usuario_id": nuevo_usuario.usuario_id
        }
    }, 201

def login_usuario(data):
    """
    Realiza el login de un usuario validando email y contraseña.
    """
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return {"mensaje": "Faltan credenciales"}, 400
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and not usuario.baja and check_password_hash(usuario.password, password):
        return {
            "mensaje": "Inicio de sesión exitoso",
            "usuario_id": usuario.usuario_id,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "rol": usuario.rol,
            "email": usuario.email
        }, 201
    else:
        return {
            "mensaje": "Credenciales incorrectas"
        }, 401