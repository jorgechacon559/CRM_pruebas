import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    # Usa el usuario de pruebas
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
    # Ajusta el ID según un usuario existente en tu base de datos de pruebas
    usuario_id = 1207  # Cambia aquí al ID de pruebas si es necesario
    response = client.post(f'/api/user/data/{usuario_id}', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (200, 404)
    # Si existe, revisa que tenga los campos esperados
    if response.status_code == 200:
        data = response.get_json()
        assert "email" in data or "nombre" in data