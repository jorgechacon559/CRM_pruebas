from datetime import datetime, date
from app.models import Ventas, DetalleVenta, Productos
from app.extensions import db
from sqlalchemy import func
from sqlalchemy.orm import joinedload

# Controlador de ventas: CRUD, paginación, estadísticas y restauración de stock

def get_all_ventas(page=1, per_page=20, usuario_id=None):
    """
    Retorna una lista paginada de ventas, opcionalmente filtrada por usuario.
    """
    try:
        query = Ventas.query.order_by(Ventas.fecha.desc())
        if usuario_id:
            query = query.filter_by(usuario_id=usuario_id)
        ventas_pag = query.paginate(page=page, per_page=per_page, error_out=False)
        ventas_data = [{
            "venta_id": v.venta_id,
            "usuario_id": v.usuario_id,
            "fecha": v.fecha.isoformat() if v.fecha else None,
            "total": float(v.total),
            "cantidad_art": v.cantidad_art
        } for v in ventas_pag.items]
        return {
            'success': True,
            'data': ventas_data,
            'total': ventas_pag.total,
            'pages': ventas_pag.pages,
            'current_page': ventas_pag.page
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_venta_by_id(venta_id):
    """
    Retorna una venta por su ID, incluyendo detalles y usuario.
    """
    try:
        venta = Ventas.query.options(
            joinedload(Ventas.detalle_ventas).joinedload(DetalleVenta.producto),
            joinedload(Ventas.usuario)
        ).filter_by(venta_id=venta_id).first()
        if not venta:
            return {"error": "Venta no encontrada"}, 404

        detalles_venta = [{
            "detalle_venta_id": detalle.detalle_venta_id,
            "cantidad": detalle.cantidad,
            "precio": detalle.precio,
            "total": detalle.total,
            "producto": {
                "producto_id": detalle.producto.producto_id,
                "nombre": detalle.producto.nombre,
                "descripcion": detalle.producto.descripcion,
                "precio": detalle.producto.precio,
                "stock": detalle.producto.stock,
                "baja": detalle.producto.baja
            }
        } for detalle in venta.detalle_ventas]

        venta_detalles_productos_usuario = {
            "venta_id": venta.venta_id,
            "detalle_usuario": {
                "usuario_id": venta.usuario.usuario_id,
                "nombre": venta.usuario.nombre,
                "apellido": venta.usuario.apellido,
                "email": venta.usuario.email,
                "baja": venta.usuario.baja
            },
            "fecha": venta.fecha.isoformat() if venta.fecha else None,
            "total": float(venta.total),
            "cantidad_art": venta.cantidad_art,
            "detalles_venta": detalles_venta
        }
        return venta_detalles_productos_usuario, 200
    except Exception as e:
        return {"error": str(e)}, 500

def get_ventas_by_cliente_id(usuario_id, page=1, per_page=20):
    """
    Retorna todas las ventas de un usuario (cliente) con paginación.
    """
    try:
        query = Ventas.query.filter_by(usuario_id=usuario_id).order_by(Ventas.fecha.desc())
        ventas_pag = query.paginate(page=page, per_page=per_page, error_out=False)
        ventas_data = [{
            "venta_id": v.venta_id,
            "usuario_id": v.usuario_id,
            "fecha": v.fecha.isoformat() if v.fecha else None,
            "total": float(v.total),
            "cantidad_art": v.cantidad_art
        } for v in ventas_pag.items]
        return {
            'success': True,
            'data': ventas_data,
            'total': ventas_pag.total,
            'pages': ventas_pag.pages,
            'current_page': ventas_pag.page
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

def create_venta(venta_data):
    """
    Crea una nueva venta, valida stock y descuenta productos.
    """
    try:
        productos_ids = [p["producto_id"] for p in venta_data["productos"]]
        productos_db = Productos.query.filter(Productos.producto_id.in_(productos_ids)).all()
        productos_db_dict = {p.producto_id: p for p in productos_db}

        # Validar stock de todos los productos antes de descontar
        for producto in venta_data["productos"]:
            prod_db = productos_db_dict.get(producto["producto_id"])
            if not prod_db:
                return {"error": f"Producto con ID {producto['producto_id']} no encontrado", "success": False}, 400
            if prod_db.stock < producto["cantidad"]:
                return {"error": f"Stock insuficiente para {prod_db.nombre}", "success": False}, 400

        venta = Ventas(
            usuario_id=venta_data["usuario_id"],
            cantidad_art=venta_data["cantidad_art"],
            total=venta_data["total"],
            fecha=venta_data["fecha"]
        )
        db.session.add(venta)
        db.session.flush()

        detalles_creados = []
        for producto in venta_data["productos"]:
            prod_db = productos_db_dict[producto["producto_id"]]
            prod_db.stock -= producto["cantidad"]

            total_detalle = producto["cantidad"] * producto["precio"]
            detalle = DetalleVenta(
                venta_id=venta.venta_id,
                producto_id=producto["producto_id"],
                cantidad=producto["cantidad"],
                precio=producto["precio"],
                total=total_detalle
            )
            db.session.add(detalle)
            detalles_creados.append({
                "producto_id": producto["producto_id"],
                "nombre": prod_db.nombre,
                "cantidad": producto["cantidad"],
                "precio": float(producto["precio"]),
                "total": float(total_detalle)
            })

        db.session.commit()
        return {
            "message": "Venta creada con éxito",
            "success": True,
            "venta": {
                "venta_id": venta.venta_id,
                "usuario_id": venta.usuario_id,
                "fecha": venta.fecha.isoformat() if hasattr(venta.fecha, 'isoformat') else venta.fecha,
                "total": float(venta.total),
                "cantidad_art": venta.cantidad_art,
                "detalles": detalles_creados
            }
        }, 201

    except KeyError as e:
        db.session.rollback()
        return {"error": f"Campo faltante: {str(e)}", "success": False}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e), "success": False}, 500

def update_venta(venta_id, venta_data):
    """
    Actualiza una venta por su ID, valida stock y restaura/descuenta productos.
    """
    try:
        venta = db.session.get(Ventas, venta_id)
        if not venta:
            return {"error": "Venta no encontrada"}, 404

        if not venta_data.get("productos"):
            return {"error": "La venta no tiene productos registrados", "success": False}, 400

        # Restaurar stock de los productos de la venta anterior
        detalles_anteriores = DetalleVenta.query.filter_by(venta_id=venta_id).all()
        for detalle in detalles_anteriores:
            producto = db.session.get(Productos, detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad

        DetalleVenta.query.filter_by(venta_id=venta_id).delete()

        productos_ids = [p["producto_id"] for p in venta_data["productos"]]
        productos_db = Productos.query.filter(Productos.producto_id.in_(productos_ids)).all()
        productos_db_dict = {p.producto_id: p for p in productos_db}

        for producto in venta_data["productos"]:
            prod_db = productos_db_dict.get(producto["producto_id"])
            if not prod_db:
                db.session.rollback()
                return {"error": f"Producto con ID {producto['producto_id']} no encontrado", "success": False}, 400
            if prod_db.stock < producto["cantidad"]:
                db.session.rollback()
                return {"error": f"Stock insuficiente para {prod_db.nombre}", "success": False}, 400

        venta.usuario_id = venta_data["usuario_id"]
        venta.cantidad_art = venta_data["cantidad_art"]
        venta.total = venta_data["total"]
        venta.fecha = venta_data["fecha"]

        detalles_creados = []
        for producto in venta_data["productos"]:
            prod_db = productos_db_dict[producto["producto_id"]]
            prod_db.stock -= producto["cantidad"]

            total_detalle = producto["cantidad"] * producto["precio"]
            detalle = DetalleVenta(
                venta_id=venta.venta_id,
                producto_id=producto["producto_id"],
                cantidad=producto["cantidad"],
                precio=producto["precio"],
                total=total_detalle
            )
            db.session.add(detalle)
            detalles_creados.append({
                "producto_id": producto["producto_id"],
                "nombre": prod_db.nombre,
                "cantidad": producto["cantidad"],
                "precio": float(producto["precio"]),
                "total": float(total_detalle)
            })

        db.session.commit()
        return {
            "message": "Venta actualizada con éxito",
            "success": True,
            "venta": {
                "venta_id": venta.venta_id,
                "usuario_id": venta.usuario_id,
                "cantidad_art": venta.cantidad_art,
                "total": venta.total,
                "fecha": venta.fecha,
                "detalles": detalles_creados
            }
        }, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_venta(venta_id):
    """
    Elimina una venta y sus detalles, restaurando el stock de los productos.
    """
    try:
        venta = db.session.get(Ventas, venta_id)
        if not venta:
            return {"error": "Venta no encontrada"}, 404

        detalles_venta = DetalleVenta.query.filter_by(venta_id=venta_id).all()
        for detalle in detalles_venta:
            producto = db.session.get(Productos, detalle.producto_id)
            if producto:
                producto.stock += detalle.cantidad
            db.session.delete(detalle)

        db.session.delete(venta)
        db.session.commit()
        return {"message": "Venta y sus detalles eliminados con éxito", "success": True}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_estadisticas_ventas(year=None):
    """
    Retorna estadísticas de ventas mensuales, productos más y menos vendidos.
    """
    try:
        if not year:
            year = datetime.now().year
        result = []

        for month in range(1, 13):
            start_date = date(year=year, month=month, day=1)
            if month == 12:
                end_date = date(year=year + 1, month=1, day=1)
            else:
                end_date = date(year=year, month=month + 1, day=1)

            ventas_mes = Ventas.query.filter(
                Ventas.fecha >= start_date,
                Ventas.fecha < end_date
            ).all()

            if not ventas_mes:
                result.append({
                    "productos_mas_vendidos": [],
                    "productos_menos_vendidos": [],
                    "ventas_totales_mes": {
                        "mes": f"{year}-{month:02d}",
                        "total_ventas": 0,
                        "total_transacciones": 0
                    }
                })
                continue

            total_ventas = sum(venta.total for venta in ventas_mes)
            total_transacciones = len(ventas_mes)

            productos_mas_vendidos = db.session.query(
                DetalleVenta.producto_id,
                Productos.nombre,
                func.sum(DetalleVenta.cantidad).label('total_vendidos')
            ).join(Productos).filter(
                DetalleVenta.venta_id.in_([v.venta_id for v in ventas_mes])
            ).group_by(DetalleVenta.producto_id, Productos.nombre
            ).order_by(func.sum(DetalleVenta.cantidad).desc()
            ).limit(5).all()

            productos_menos_vendidos = db.session.query(
                DetalleVenta.producto_id,
                Productos.nombre,
                func.sum(DetalleVenta.cantidad).label('total_vendidos')
            ).join(Productos).filter(
                DetalleVenta.venta_id.in_([v.venta_id for v in ventas_mes])
            ).group_by(DetalleVenta.producto_id, Productos.nombre
            ).order_by(func.sum(DetalleVenta.cantidad).asc()
            ).limit(5).all()

            result.append({
                "productos_mas_vendidos": [
                    {
                        "producto_id": p.producto_id,
                        "nombre": p.nombre,
                        "total_vendidos": p.total_vendidos
                    } for p in productos_mas_vendidos
                ],
                "productos_menos_vendidos": [
                    {
                        "producto_id": p.producto_id,
                        "nombre": p.nombre,
                        "total_vendidos": p.total_vendidos
                    } for p in productos_menos_vendidos
                ],
                "ventas_totales_mes": {
                    "mes": f"{year}-{month:02d}",
                    "total_ventas": round(total_ventas, 2),
                    "total_transacciones": total_transacciones
                }
            })

        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500