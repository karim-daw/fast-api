from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings



# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# use conenction string in engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependancy
# The session object talks to databse, we get a session for the database everytime we get request
# more efficient, we keep calling this function everytime we get a request to api end points
def overid_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()








client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.json().get('message') == "Hello World, im Karim!!!"
    assert res.status_code == 200

def test_create_user():
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password":"password123"})

    # this will automatically do valiadation for us with all user out attributes
    new_user = schemas.UserOut(**res.json())
    print(new_user)

    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

    

