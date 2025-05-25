from app.models import DetalleVenta
from app.extensions import db

# Controlador de detalles de venta: CRUD y consulta

def get_all_detalle_ventas():
    """
    Retorna todos los detalles de venta.
    """
    try:
        detalle_venta = DetalleVenta.query.all()
        detalles = [{
            "detalle_venta_id": detalle.detalle_venta_id,
            "venta_id": detalle.venta_id,
            "producto_id": detalle.producto_id,
            "cantidad": detalle.cantidad,
            "precio": detalle.precio,
            "total": detalle.total,
        } for detalle in detalle_venta]
        return detalles, 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_detalle_venta_by_id(id):
    """
    Retorna un detalle de venta por su ID.
    """
    try:
        detalle_venta = db.session.get(DetalleVenta, id)
        if detalle_venta:
            return {
                "detalle_venta": {
                    "detalle_venta_id": detalle_venta.detalle_venta_id,
                    "venta_id": detalle_venta.venta_id,
                    "producto_id": detalle_venta.producto_id,
                    "cantidad": detalle_venta.cantidad,
                    "precio": detalle_venta.precio,
                    "total": detalle_venta.total,
                }
            }, 200
        else:
            return {'message': 'Detalle de venta no encontrado'}, 404
    except Exception as e:
        return {"error": str(e)}, 500

def create_detalle_venta(detalle_venta):
    """
    Crea un nuevo detalle de venta.
    """
    try:
        campos_obligatorios = ["venta_id", "producto_id", "cantidad", "precio", "total"]
        for campo in campos_obligatorios:
            if campo not in detalle_venta:
                return {"error": f"Falta el campo obligatorio '{campo}'"}, 400

        if detalle_venta["cantidad"] <= 0:
            return {"error": "La cantidad debe ser mayor a cero."}, 400
        if detalle_venta["precio"] < 0:
            return {"error": "El precio no puede ser negativo."}, 400
        if detalle_venta["total"] < 0:
            return {"error": "El total no puede ser negativo."}, 400

        new_detalle_venta = DetalleVenta(
            venta_id=detalle_venta['venta_id'],
            producto_id=detalle_venta['producto_id'],
            cantidad=detalle_venta['cantidad'],
            precio=detalle_venta['precio'],
            total=detalle_venta['total'],
        )
        db.session.add(new_detalle_venta)
        db.session.commit()
        return {
            "message": "Detalle de venta creado exitosamente",
            "detalle_venta": {
                "detalle_venta_id": new_detalle_venta.detalle_venta_id,
                "venta_id": new_detalle_venta.venta_id,
                "producto_id": new_detalle_venta.producto_id,
                "cantidad": new_detalle_venta.cantidad,
                "precio": new_detalle_venta.precio,
                "total": new_detalle_venta.total,
            }
        }, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def update_detalle_venta(id, detalle_venta):
    """
    Actualiza un detalle de venta por su ID.
    """
    try:
        detalle_venta_db = db.session.get(DetalleVenta, id)
        if not detalle_venta_db:
            return {'message': 'Detalle de venta no encontrado'}, 404

        detalle_venta_db.venta_id = detalle_venta['venta_id']
        detalle_venta_db.producto_id = detalle_venta['producto_id']
        detalle_venta_db.cantidad = detalle_venta['cantidad']
        detalle_venta_db.precio = detalle_venta['precio']
        detalle_venta_db.total = detalle_venta['total']

        db.session.add(detalle_venta_db)
        db.session.commit()
        return {
            "detalle_venta": {
                "detalle_venta_id": detalle_venta_db.detalle_venta_id,
                "venta_id": detalle_venta_db.venta_id,
                "producto_id": detalle_venta_db.producto_id,
                "cantidad": detalle_venta_db.cantidad,
                "precio": detalle_venta_db.precio,
                "total": detalle_venta_db.total,
            }
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_detalle_venta(id):
    """
    Elimina un detalle de venta por su ID.
    """
    try:
        detalle_venta_db = db.session.get(DetalleVenta, id)
        if not detalle_venta_db:
            return {'message': 'Detalle de venta no encontrado'}, 404

        db.session.delete(detalle_venta_db)
        db.session.commit()
        return {'message': 'Detalle de venta eliminado'}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500