# -*- coding: utf-8 -*-
# You can define fixtures here all tests will have access to them automatically
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

# Setup  test db for test
# you should create new database for test in tableplus or your db manager

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# add scope="module" so the fixture is only executed once in the module
# https://youtu.be/0sOvCWFmrtA?t=57683


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# create fixture for cerating user


@pytest.fixture
def test_create_login_user(client):
    user_data = {"email": "test@test.se", "password": "test_password"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


# create fixture for authenticating user


@pytest.fixture
def token(test_create_login_user):
    return create_access_token({"user_id": test_create_login_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    # client.headers = {
    #     **client.headers,
    #     "Authorization": f"Bearer {token}"
    # }
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


# create fixture for creating test posts


@pytest.fixture
def test_posts(test_create_login_user, session):
    post_data = [
        {
            "title": "Test title",
            "content": "Test content",
            "owner_id": test_create_login_user["id"],
        },
        {
            "title": "Test title 2",
            "content": "Test content 2",
            "owner_id": test_create_login_user["id"],
        },
        {
            "title": "Test title 3",
            "content": "Test content 3",
            "owner_id": test_create_login_user["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, post_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()
