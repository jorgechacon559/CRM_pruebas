def get_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    return response.get_json()["access_token"]

def test_create_venta(client):
    token = get_token(client)
    producto = {
        "nombre": "Producto Venta",
        "descripcion": "Producto para venta",
        "precio": 20.0,
        "stock": 100,
        "baja": False
    }
    prod_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    producto_id = prod_resp.get_json()["producto"]["producto_id"]

    venta = {
        "usuario_id": 1207,
        "cantidad_art": 2,
        "total": 40.0,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 2,
                "precio": 20.0
            }
        ]
    }
    response = client.post('/api/ventas', json=venta, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 201)
    data = response.get_json()
    assert "venta" in data or "message" in data

def test_get_all_ventas(client):
    token = get_token(client)
    response = client.get('/api/ventas', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data or "ventas" in data

def test_get_ventas_by_usuario(client):
    token = get_token(client)
    usuario_id = 1207
    response = client.get(f'/api/ventas/usuario/{usuario_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "data" in data or "ventas" in data

def test_update_venta(client):
    token = get_token(client)
    producto = {
        "nombre": "Producto Venta Update",
        "descripcion": "Producto para venta update",
        "precio": 30.0,
        "stock": 50,
        "baja": False
    }
    prod_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    producto_id = prod_resp.get_json()["producto"]["producto_id"]

    venta = {
        "usuario_id": 1207,
        "cantidad_art": 1,
        "total": 30.0,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 1,
                "precio": 30.0
            }
        ]
    }
    create_resp = client.post('/api/ventas', json=venta, headers={
        "Authorization": f"Bearer {token}"
    })
    venta_id = create_resp.get_json()["venta"]["venta_id"]

    update_data = {
        "usuario_id": 1207,
        "cantidad_art": 2,
        "total": 60.0,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 2,
                "precio": 30.0
            }
        ]
    }
    update_resp = client.put(f'/api/ventas/{venta_id}', json=update_data, headers={
        "Authorization": f"Bearer {token}"
    })
    assert update_resp.status_code == 200
    updated = update_resp.get_json()
    assert "venta" in updated or "message" in updated

def test_delete_venta(client):
    token = get_token(client)
    producto = {
        "nombre": "Producto Venta Delete",
        "descripcion": "Producto para venta delete",
        "precio": 15.0,
        "stock": 10,
        "baja": False
    }
    prod_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    producto_id = prod_resp.get_json()["producto"]["producto_id"]

    venta = {
        "usuario_id": 1207,
        "cantidad_art": 1,
        "total": 15.0,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 1,
                "precio": 15.0
            }
        ]
    }
    create_resp = client.post('/api/ventas', json=venta, headers={
        "Authorization": f"Bearer {token}"
    })
    venta_id = create_resp.get_json()["venta"]["venta_id"]

    delete_resp = client.delete(f'/api/ventas/{venta_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert delete_resp.status_code == 200
    assert "eliminados" in delete_resp.get_json().get("message", "")

def test_create_venta_stock_insuficiente(client):
    token = get_token(client)
    producto = {
        "nombre": "Producto Sin Stock",
        "descripcion": "Producto sin stock suficiente",
        "precio": 100.0,
        "stock": 1,
        "baja": False
    }
    prod_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    producto_id = prod_resp.get_json()["producto"]["producto_id"]

    venta = {
        "usuario_id": 1207,
        "cantidad_art": 2,
        "total": 200.0,
        "fecha": "2024-05-23",
        "productos": [
            {
                "producto_id": producto_id,
                "cantidad": 2,
                "precio": 100.0
            }
        ]
    }
    response = client.post('/api/ventas', json=venta, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (400, 409)
    assert "stock" in response.get_json().get("error", "").lower()