
from flask import Blueprint, jsonify
from app.controllers import dashboard_controller

dashboard_api = Blueprint("dashboard_api", __name__)

@dashboard_api.route('/summary', methods=['GET'])
def resumen_dashboard():
    data = dashboard_controller.obtener_resumen_dashboard()
    return jsonify(data)

@dashboard_api.route('/ventas-recientes', methods=['GET'])
def ventas_recientes():
    data = dashboard_controller.obtener_ventas_recientes()
    return jsonify(data)

@dashboard_api.route('/ventas-semana', methods=['GET'])
def ventas_por_dia():
    data = dashboard_controller.obtener_ventas_por_dia()
    return jsonify(data)

@dashboard_api.route('/producto-top', methods=['GET'])
def producto_top():
   data = dashboard_controller.obtener_producto_top()
   return jsonify(data)

@dashboard_api.route('/productos-top-5', methods=['GET'])
def productos_top_5():
    data = dashboard_controller.obtener_top_5_productos_semana()
    return jsonify(data)
