from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# use conenction string in engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# fixture that returns database
@pytest.fixture(scope="function")
def session():
    # this will drop test db with all our tables
    Base.metadata.drop_all(bind=engine)
    # this will populate test db with all our tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# fixture that returns client
@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    # overriding database dependancy
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):

    # create dummy user data
    user_data = {
        "email": "hello123@gmail.com",
        "password": "password123"
    }
    # create user with api
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    # we pass in password too because doesnt its not ruturned in create user 
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

def test_incorrect_login(test_user, client):
    res = client.post("/login",
        data = {
            "username": test_user['email'],
            "password": test_user["wrong passowrd"]
        })
    assert res.status_code == 403
    assert res.json().get('detail') == 'Invalid Credentials'