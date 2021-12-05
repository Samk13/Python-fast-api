from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get('message') == "Hello World during the coronavirus pandemic! 🎉"


def test_create_user():
    res = client.post(
        "/users/", json={"email": "test1@test.se", "password": "test_password"})
    assert res.status_code == 201
