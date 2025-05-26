#controllers/dashboard_controller
from datetime import datetime, timedelta
from sqlalchemy import func
from app.extensions import db
from app.models.productos import Productos
from app.models.ventas import Ventas
from app.models.detalle_venta import DetalleVenta
from app.models.usuario import Usuario

def obtener_resumen_dashboard():
    total_productos = Productos.query.filter(Productos.baja == False, Productos.stock > 0).count()
    
    hace_una_semana = datetime.now() - timedelta(days=7)
    ventas_semana = Ventas.query.filter(Ventas.fecha >= hace_una_semana).all()
    total_ventas_semana = len(ventas_semana)
    ingresos_totales = sum([venta.total for venta in ventas_semana])

    return {
        "total_productos": total_productos,
        "ventas_semana": total_ventas_semana,
        "ingresos_totales": ingresos_totales
    }

def obtener_ventas_recientes(limit=10):
    ventas = (
        db.session.query(Ventas, Usuario)
        .join(Usuario, Usuario.usuario_id == Ventas.usuario_id)
        .order_by(Ventas.fecha.desc())
        .limit(limit)
        .all()
    )
    
    resultado = [
        {
            "fecha": v.fecha.strftime("%Y-%m-%d"),
            "usuario": f"{u.nombre} {u.apellido}",
            "total": v.total
        }
        for v, u in ventas
    ]

    return resultado

def obtener_ventas_por_dia():
    hace_una_semana = datetime.now() - timedelta(days=7)
    ventas = (
        db.session.query(func.date(Ventas.fecha), func.sum(Ventas.total))
        .filter(Ventas.fecha >= hace_una_semana)
        .group_by(func.date(Ventas.fecha))
        .order_by(func.date(Ventas.fecha))
        .all()
    )
    return [{"fecha": str(f[0]), "total": f[1]} for f in ventas]

def obtener_top_5_productos_semana():
    hace_una_semana = datetime.now() - timedelta(days=7)
    productos = (
        db.session.query(
            DetalleVenta.producto_id,
            Productos.nombre,
            func.sum(DetalleVenta.cantidad).label("cantidad_total")
        )
        .join(Productos, Productos.producto_id == DetalleVenta.producto_id)
        .join(Ventas, Ventas.venta_id == DetalleVenta.venta_id)
        .filter(Ventas.fecha >= hace_una_semana)
        .group_by(DetalleVenta.producto_id, Productos.nombre)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "producto_id": p.producto_id,
            "nombre": p.nombre,
            "cantidad_vendida": int(p.cantidad_total)
        }
        for p in productos
    ]

def obtener_producto_top():
    top5 = obtener_top_5_productos_semana()
    if top5:
        return top5[0]
    return {}
