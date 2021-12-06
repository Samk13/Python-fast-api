from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
# Setup  test db for test
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
)
testingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)


def override_get_db():
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Swapping out the get_db function with the testing one
app.dependency_overrides[get_db] = override_get_db

# End setup test db for test

# Setup fixture for test


@pytest.fixture
def client():
    # drop tables
    Base.metadata.drop_all(bind=engine)
    # create tables
    Base.metadata.create_all(bind=engine)
# Change return to yield so we can run code before and after the testClient
    yield TestClient(app)


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
