from app import schemas
from jose import jwt
from app.config import settings

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


def test_login_user(client, test_create_login_user):
    res = client.post(
        "/login",
        data={
            "username": test_create_login_user["email"],
            "password": test_create_login_user["password"],
        },
    )
    login_res = schemas.TokenResponse(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_create_login_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
