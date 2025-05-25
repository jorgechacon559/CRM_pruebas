def get_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    return response.get_json()["access_token"]

def test_get_estadisticas(client):
    token = get_token(client)
    response = client.get('/api/ventas/data', headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        for mes in data:
            assert "productos_mas_vendidos" in mes
            assert "productos_menos_vendidos" in mes
            assert "ventas_totales_mes" in mes

def test_estadisticas_protegido(client):
    response = client.get('/api/ventas/data')
    assert response.status_code in (401, 403)

def test_chatbot_saludo(client):
    token = get_token(client)
    response = client.post('/api/chatbot', json={
        "consulta": "Hola"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["exito"] is True
    assert "teo" in data["respuesta"].lower() or "asistente" in data["respuesta"].lower()

def test_chatbot_producto_mas_vendido(client):
    token = get_token(client)
    response = client.post('/api/chatbot', json={
        "consulta": "¿Cuál es mi producto más vendido?"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["exito"] is True
    assert any(char.isalpha() for char in data["respuesta"])

def test_chatbot_productos_agotados(client):
    token = get_token(client)
    response = client.post('/api/chatbot', json={
        "consulta": "¿Qué productos están agotados?"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["exito"] is True
    assert "agotado" in data["respuesta"].lower() or "bajo stock" in data["respuesta"].lower()