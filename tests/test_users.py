from app import schemas
from .database import client, session
#  should import session even though it's not called directly cuase client is dependent on it


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json().get("message") == "Hello World during the coronavirus pandemic! 🎉"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test@test.se", "password": "test_password"}
    )
    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert res.json().get("email") == "test@test.se"
