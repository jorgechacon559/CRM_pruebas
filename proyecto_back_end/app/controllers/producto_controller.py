from app.models import Productos
from app.extensions import db

## Retornar una lista de todos los productos
def get_all_productos():
    try:
        productos = Productos.query.filter(Productos.baja == False).all()
        return {
            "productos": [
                {
                    "producto_id": producto.producto_id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                    "baja": producto.baja,
                }
                for producto in productos
            ]
        }, 201
    except Exception as e:
        return {"error": str(e)}, 500  

#Retornar un producto por su ID
def get_producto_by_id(id):
    try:
        producto = db.session.get(Productos, id)
        return {
            "producto" : {
                "producto_id" : producto.producto_id,  
                "nombre": producto.nombre,
                "descripcion": producto.descripcion,
                "precio": producto.precio,
                "stock": producto.stock,              
                "baja": producto.baja,
            }
        }
    except Exception as e:
        return {"error": str(e)}, 500  
    
# Crear un nuevo producto
def create_producto(data):
    try:
        nuevo_producto = Productos(**data)
        db.session.add(nuevo_producto)
        db.session.commit()
        return {
            "message": "Producto registrado",
            "producto": {
                "producto_id": nuevo_producto.producto_id,
                "nombre": nuevo_producto.nombre,
                "descripcion": nuevo_producto.descripcion,
                "precio": nuevo_producto.precio,
                "stock": nuevo_producto.stock,
            }
        }, 201
    except Exception as e:
        return {"error": str(e)}, 500
    
# Actualizar un producto por su ID
def update_producto(id, data):
    try:
        producto = db.session.get(Productos, id)
        if not producto:
            return {'error': 'Producto no encontrado'}, 404
        else:
            producto.nombre = data['nombre']
            producto.descripcion = data['descripcion']
            producto.precio = data['precio']
            producto.stock = data['stock']
            
            db.session.add(producto)
            db.session.commit()
            return {
                "message": "Producto actualizado",
                "producto": {
                    "producto_id": producto.producto_id,
                    "nombre": producto.nombre,
                    "descripcion": producto.descripcion,
                    "precio": producto.precio,
                    "stock": producto.stock,
                }
            }, 200
    except Exception as e:
        return {"error": str(e)}, 500   

# Eliminar un producto por su ID
def delete_producto(id):
    try:
        producto = db.session.get(Productos, id)        
        if not producto:
            return {'error': 'Producto no encontrado'}, 404
        else:
            producto.baja = True  # <-- Solo marca como dado de baja
            db.session.add(producto)
            db.session.commit()
            return {
                "message": "Producto dado de baja (baja lógica)"
            }, 200
    except Exception as e:
        db.session.rollback()
        print("Error al eliminar producto:", e)
        return {"error": "Error interno del servidor. Detalles: " + str(e)}, 500