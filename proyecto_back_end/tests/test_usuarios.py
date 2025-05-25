def get_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    return response.get_json()["access_token"]

def test_get_all_usuarios(client):
    token = get_token(client)
    response = client.get('/api/usuarios', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list) or isinstance(data, dict)

def test_get_usuario_by_id(client):
    token = get_token(client)
    usuario_id = 1207  # Cambiar aquí al ID de pruebas según si es necesario
    response = client.post(f'/api/user/data/{usuario_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.get_json()
        assert "email" in data or "nombre" in data