from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# use conenction string in engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# fixture that returns database
@pytest.fixture()
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


@pytest.fixture()
def client(session):
    """fixture that returns app client"""
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
    """fixture that creates test user"""

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


@pytest.fixture()
def token(test_user):
    """fixture that creates taken from test_user fixture"""
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    # update client headers
    # take original client headers and simply adding Authorization header
    # from token dixture
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    },{
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]

    # decompose **kwargs for models.Post() for each entry, conver to list, add to db
    posts = list(map(lambda post: models.Post(**post), posts_data))
    session.add_all(posts)
    session.commit()