import uuid

USUARIO_PRUEBA = {
    "email": "pruebas@test.net",
    "password": "pruebas1"
}
USUARIO_ID = 1207

def get_token(client):
    resp = client.post('/api/login', json=USUARIO_PRUEBA)
    assert resp.status_code == 200
    return resp.get_json()["access_token"]

def crear_producto(client, token, nombre=None, precio=50.0, stock=20):
    if not nombre:
        nombre = f"Producto DetalleVenta {uuid.uuid4()}"
    producto = {
        "nombre": nombre,
        "descripcion": "Producto para detalle venta",
        "precio": precio,
        "stock": stock,
        "baja": False
    }
    resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in (200, 201), f"Respuesta inesperada: {resp.get_json()}"
    return resp.get_json()["producto"]["producto_id"]

def crear_venta(client, token, producto_id, cantidad=1, precio=50.0):
    venta = {
        "usuario_id": USUARIO_ID,
        "cantidad_art": cantidad,
        "total": cantidad * precio,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": cantidad,
                "precio": precio
            }
        ]
    }
    resp = client.post('/api/ventas', json=venta, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in (200, 201)
    return resp.get_json()["venta"]["venta_id"]

def crear_detalle_venta(client, token, venta_id, producto_id, cantidad=1, precio=50.0):
    detalle = {
        "venta_id": venta_id,
        "producto_id": producto_id,
        "cantidad": cantidad,
        "precio": precio,
        "total": cantidad * precio
    }
    resp = client.post('/api/detalle_venta', json=detalle, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in (200, 201)
    return resp.get_json()["detalle_venta"]["detalle_venta_id"]

def test_crud_detalle_venta(client):
    token = get_token(client)
    producto_id = crear_producto(client, token)
    venta_id = crear_venta(client, token, producto_id)
    detalle_id = crear_detalle_venta(client, token, venta_id, producto_id)

    resp = client.get('/api/detalle_venta', headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    assert isinstance(resp.get_json(), list)

    resp = client.get(f'/api/detalle_venta/{detalle_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "detalle_venta" in data
    assert data["detalle_venta"]["detalle_venta_id"] == detalle_id

    update_data = {
        "venta_id": venta_id,
        "producto_id": producto_id,
        "cantidad": 3,
        "precio": 50.0,
        "total": 150.0
    }
    resp = client.put(f'/api/detalle_venta/{detalle_id}', json=update_data, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    updated = resp.get_json()["detalle_venta"]
    assert updated["cantidad"] == 3
    assert updated["total"] == 150.0

    resp = client.delete(f'/api/detalle_venta/{detalle_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    assert "eliminado" in resp.get_json().get("message", "").lower()

def test_detalle_venta_validaciones(client):
    token = get_token(client)
    producto_id = crear_producto(client, token)
    venta_id = crear_venta(client, token, producto_id)

    detalle = {
        "venta_id": venta_id,
        "cantidad": 1,
        "precio": 50.0,
        "total": 50.0
    }
    resp = client.post('/api/detalle_venta', json=detalle, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in (400, 422, 500)

    detalle = {
        "venta_id": venta_id,
        "producto_id": producto_id,
        "cantidad": -2,
        "precio": 50.0,
        "total": -100.0
    }
    resp = client.post('/api/detalle_venta', json=detalle, headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code in (400, 422, 500)

def test_detalle_venta_protegido(client):
    resp = client.get('/api/detalle_venta')
    assert resp.status_code in (401, 403)