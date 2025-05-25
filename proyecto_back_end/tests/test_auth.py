def test_login_success(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_fail(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "contraseña_incorrecta"
    })
    assert response.status_code == 401

def test_register_success(client):
    import uuid
    email = f"test_{uuid.uuid4().hex[:8]}@mail.com"
    response = client.post('/api/registrar', json={
        "email": email,
        "password": "123456",
        "nombre": "Test",
        "apellido": "User"
    })
    assert response.status_code in (200, 201, 202)

def test_register_fail_duplicate(client):
    email = "duplicado@prueba.com"
    client.post('/api/registrar', json={
        "email": email,
        "password": "123456",
        "nombre": "Test",
        "apellido": "User"
    })
    response = client.post('/api/registrar', json={
        "email": email,
        "password": "123456",
        "nombre": "Test",
        "apellido": "User"
    })
    assert response.status_code in (400, 409, 401)

def test_refresh_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    assert response.status_code == 200
    refresh_token = response.get_json().get("refresh_token")
    assert refresh_token
    response = client.post('/api/refresh', headers={
        "Authorization": f"Bearer {refresh_token}"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()

def test_protected_endpoint_requires_token(client):
    response = client.get('/api/usuarios')
    assert response.status_code == 401