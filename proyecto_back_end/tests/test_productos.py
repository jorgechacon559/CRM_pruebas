import uuid

def get_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    return response.get_json()["access_token"]

def test_create_producto(client):
    token = get_token(client)
    producto = {
        "nombre": f"Producto Test {uuid.uuid4()}",
        "descripcion": "Descripción de prueba",
        "precio": 99.99,
        "stock": 10,
        "baja": False
    }
    response = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 201)
    data = response.get_json()
    assert "producto" in data, f"Respuesta inesperada: {data}"
    assert data["producto"]["nombre"] == producto["nombre"]

def test_get_all_productos(client):
    token = get_token(client)
    response = client.get('/api/productos', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 201)
    data = response.get_json()
    assert "productos" in data
    assert isinstance(data["productos"], list)

def test_update_producto(client):
    token = get_token(client)
    producto = {
        "nombre": f"Producto Update {uuid.uuid4()}",
        "descripcion": "Desc update",
        "precio": 50.0,
        "stock": 5,
        "baja": False
    }
    create_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    data = create_resp.get_json()
    assert "producto" in data, f"Respuesta inesperada: {data}"
    producto_id = data["producto"]["producto_id"]

    update_data = {
        "nombre": "Producto Actualizado",
        "descripcion": "Desc actualizada",
        "precio": 75.0,
        "stock": 8,
        "baja": False
    }
    update_resp = client.put(f'/api/productos/{producto_id}', json=update_data, headers={
        "Authorization": f"Bearer {token}"
    })
    assert update_resp.status_code == 200
    updated = update_resp.get_json()["producto"]
    assert updated["nombre"] == "Producto Actualizado"
    assert updated["precio"] == 75.0

def test_delete_producto(client):
    token = get_token(client)
    producto = {
        "nombre": f"Producto Delete {uuid.uuid4()}",
        "descripcion": "Desc delete",
        "precio": 10.0,
        "stock": 2,
        "baja": False
    }
    create_resp = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    data = create_resp.get_json()
    assert "producto" in data, f"Respuesta inesperada: {data}"
    producto_id = data["producto"]["producto_id"]

    delete_resp = client.delete(f'/api/productos/{producto_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert delete_resp.status_code == 200
    assert "Producto dado de baja" in delete_resp.get_json()["message"]

def test_create_producto_faltan_campos(client):
    token = get_token(client)
    producto = {
        "descripcion": "Sin nombre",
        "precio": 10.0,
        "stock": 1,
        "baja": False
    }
    response = client.post('/api/productos', json=producto, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (400, 500)