import email
import pytest
from app import schemas
from .database import client, session


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

    
def test_login_user(client, test_user):

    # data is for formdata, json is for jsondata
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    print(res.json())
    assert res.status_code == 200

