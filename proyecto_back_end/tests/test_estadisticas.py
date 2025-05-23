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