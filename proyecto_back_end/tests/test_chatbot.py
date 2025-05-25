def get_token(client):
    response = client.post('/api/login', json={
        "email": "pruebas@test.net",
        "password": "pruebas1"
    })
    return response.get_json()["access_token"]

def test_chatbot_responde_a_consulta(client):
    token = get_token(client)
    consulta = "¿Cuál es el producto más vendido?"
    response = client.post('/api/chatbot', json={
        "consulta": consulta
    }, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "exito" in data
    assert data["exito"] is True
    assert "respuesta" in data
    assert isinstance(data["respuesta"], str)
    assert len(data["respuesta"]) > 0

def test_chatbot_falta_consulta(client):
    token = get_token(client)
    response = client.post('/api/chatbot', json={}, headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code in (400, 422)
    data = response.get_json()
    assert "error" in data or "exito" in data

def test_chatbot_protegido(client):
    response = client.post('/api/chatbot', json={
        "consulta": "¿Quién eres?"
    })
    assert response.status_code in (401, 403)