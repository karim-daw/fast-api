from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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



# Dependancy
# The session object talks to databse, we get a session for the database everytime we get request
# more efficient, we keep calling this function everytime we get a request to api end points
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# overriding database dependancy
# this will swap the dependancies out so that we can use a test
app.dependency_overrides[get_db] = override_get_db

# fixtures
@pytest.fixture
def client():
    # run our code before we run our test
    # this will populate test db with all our tables
    Base.metadata.create_all(bind=engine)

    yield TestClient(app)

    # run our code after our test finishes
    # this will populate test db with all our tables
    Base.metadata.drop_all(bind=engine)

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Hello World, im Karim!!!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password":"password123"})

    # this will automatically do valiadation for us with all user out attributes
    new_user = schemas.UserOut(**res.json())

    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

    

