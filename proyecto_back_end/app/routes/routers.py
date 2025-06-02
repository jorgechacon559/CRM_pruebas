from flask import Blueprint, jsonify, request
from ..controllers import usuario_controller, producto_controller, venta_controller, chat_bot_controller, venta_detalle_controller
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    resultado, status_code = usuario_controller.login_usuario(data)
    if status_code == 201:
        usuario_id = resultado.get("usuario_id")
        access_token = create_access_token(identity=str(usuario_id))
        refresh_token = create_refresh_token(identity=str(usuario_id))
        return jsonify({
            "mensaje": resultado["mensaje"],
            "access_token": access_token,
            "refresh_token": refresh_token,
            "usuario_id": usuario_id,
            "nombre": resultado.get("nombre"),
            "apellido": resultado.get("apellido"),
            "rol": resultado.get("rol"),
            "email": resultado.get("email")
        }), 200
    else:
        return jsonify(resultado), 401

@api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=str(current_user))
    return jsonify(access_token=new_access_token), 200

@api.route('/registrar', methods=['POST'])
def register_user():
    data = request.get_json()
    resultado, status_code = usuario_controller.registrar_usuario(data)
    return jsonify(resultado), status_code

@api.route('/usuarios', methods=['GET'])
@jwt_required()
def get_all_data():
    current_user_id = get_jwt_identity()
    usuario, _ = usuario_controller.get_data_usuario(current_user_id)
    print("ROL DEL USUARIO AUTENTICADO:", usuario.get("rol"))
    if not usuario or usuario.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403
    usuarios, status_code = usuario_controller.get_all_users()
    return jsonify(usuarios), status_code

@api.route('/user/data/<int:usuario_id>', methods=['POST'])
@jwt_required()
def get_data_usuario(usuario_id):
    usuario, status_code = usuario_controller.get_data_usuario(usuario_id)
    return jsonify(usuario), status_code

@api.route('/productos', methods=['GET'])
@jwt_required()
def get_all_productos():
    productos, status_code = producto_controller.get_all_productos()
    return jsonify(productos), status_code

@api.route('/productos/<int:producto_id>', methods=['GET'])
@jwt_required()
def get_producto(producto_id):
    producto, status_code = producto_controller.get_producto_by_id(producto_id)
    return jsonify(producto), status_code

@api.route('/productos', methods=['POST'])
@jwt_required()
def create_producto():
    data = request.get_json()
    producto, status_code = producto_controller.create_producto(data)
    return jsonify(producto), status_code

@api.route('/productos/<int:producto_id>', methods=['PUT'])
@jwt_required()
def update_producto(producto_id):
    data = request.get_json()
    producto, status_code = producto_controller.update_producto(producto_id, data)
    return jsonify(producto), status_code

@api.route('/productos/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def delete_producto(producto_id):
    producto, status_code = producto_controller.delete_producto(producto_id)
    return jsonify(producto), status_code

@api.route('/ventas', methods=['GET'])
@jwt_required()
def get_all_ventas():
    page = int(request.args.get('page', 1))
    ventas, status_code = venta_controller.get_all_ventas(page=page)
    return jsonify(ventas), status_code

@api.route('/ventas/<int:venta_id>', methods=['GET'])
@jwt_required()
def get_venta(venta_id):
    data, status_code = venta_controller.get_venta_by_id(venta_id)
    return jsonify(data), status_code

@api.route('/ventas/usuario/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_venta_by_usuario(usuario_id):
    ventas, status_code = venta_controller.get_ventas_by_cliente_id(usuario_id)
    return jsonify(ventas), status_code

@api.route('/ventas', methods=['POST'])
@jwt_required()
def create_venta():
    data = request.get_json()
    venta, status_code = venta_controller.create_venta(data)
    return jsonify(venta), status_code

@api.route('/ventas/<int:venta_id>', methods=['PUT'])
@jwt_required()
def update_venta(venta_id):
    data = request.get_json()
    venta, status_code = venta_controller.update_venta(venta_id, data)
    return jsonify(venta), status_code

@api.route('/ventas/<int:venta_id>', methods=['DELETE'])
@jwt_required()
def delete_venta(venta_id):
    venta, status_code = venta_controller.delete_venta(venta_id)
    return jsonify(venta), status_code

@api.route('/ventas/data', methods=['GET'])
@jwt_required()
def get_all_stadistics():
    ventas, status_code = venta_controller.get_estadisticas_ventas()
    return jsonify(ventas), status_code

@api.route('/chatbot', methods=['POST'])
@jwt_required()
def procesar_consulta_chatbot():
    data = request.get_json()
    if not data or "consulta" not in data:
        return jsonify({"error": "Falta el campo 'consulta'"}), 400

    datos_ventas = chat_bot_controller.obtener_datos_ventas(data, venta_controller.get_estadisticas_ventas)
    print("DATOS QUE SE ENVIAN AL BOT:", datos_ventas)
    respuesta = chat_bot_controller.chat_bot(data, datos_ventas)
    return jsonify({
        "exito": respuesta.get("success", False),
        "respuesta": respuesta.get("data", "")
    }), 200

@api.route('/detalle_venta', methods=['GET'])
@jwt_required()
def get_all_detalle_ventas():
    detalle_ventas, status_code = venta_detalle_controller.get_all_detalle_ventas()
    return jsonify(detalle_ventas), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['GET'])
@jwt_required()
def get_detalle_venta_by_id(venta_detalle_id):
    detalle_venta, status_code = venta_detalle_controller.get_detalle_venta_by_id(venta_detalle_id)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta', methods=['POST'])
@jwt_required()
def create_detalle_venta():
    data = request.get_json()
    detalle_venta, status_code = venta_detalle_controller.create_detalle_venta(data)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['PUT'])
@jwt_required()
def update_detalle_venta(venta_detalle_id):
    data = request.get_json()
    detalle_venta, status_code = venta_detalle_controller.update_detalle_venta(venta_detalle_id, data)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['DELETE'])
@jwt_required()
def delete_detalle_venta(venta_detalle_id):
    detalle_venta, status_code = venta_detalle_controller.delete_detalle_venta(venta_detalle_id)
    return jsonify(detalle_venta), status_code

@api.route('/usuarios/<int:usuario_id>/hacer-admin', methods=['PUT'])
@jwt_required()
def hacer_admin(usuario_id):
    current_user_id = get_jwt_identity()
    usuario_actual, _ = usuario_controller.get_data_usuario(current_user_id)
    if not usuario_actual or usuario_actual.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403

    if int(current_user_id) == int(usuario_id):
        return jsonify({"error": "No puedes ascenderte a ti mismo"}), 400

    usuario, status = usuario_controller.get_data_usuario(usuario_id)
    if status != 200:
        return jsonify({"error": "Usuario no encontrado"}), 404

    from app.models import Usuario
    user_obj = Usuario.query.get(usuario_id)
    if user_obj.rol == "admin":
        return jsonify({"msg": "El usuario ya es admin"}), 200

    user_obj.rol = "admin"
    from app.extensions import db
    db.session.commit()
    return jsonify({"msg": "Usuario ascendido a admin"}), 200

@api.route('/usuarios/<int:usuario_id>/baja', methods=['PUT'])
@jwt_required()
def baja_usuario(usuario_id):
    current_user_id = get_jwt_identity()
    usuario_actual, _ = usuario_controller.get_data_usuario(current_user_id)
    if not usuario_actual or usuario_actual.get("rol") != "admin":
        return jsonify({"error": "Acceso denegado: se requiere rol de administrador"}), 403

    usuario, status = usuario_controller.get_data_usuario(usuario_id)
    if status != 200:
        return jsonify({"error": "Usuario no encontrado"}), 404

    from app.models import Usuario
    user_obj = Usuario.query.get(usuario_id)
    if user_obj.baja:
        return jsonify({"msg": "El usuario ya está dado de baja"}), 200

    user_obj.email = f"{user_obj.email}_baja_{usuario_id}"
    user_obj.baja = True
    from app.extensions import db
    db.session.commit()
    return jsonify({"msg": "Usuario dado de baja"}), 200