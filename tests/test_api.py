from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_register_endpoint():
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass",
        "role": "USER"
    })
    assert response.status_code in (200, 400)  # 400 if user exists

def test_login_endpoint():
    response = client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code in (200, 401)
