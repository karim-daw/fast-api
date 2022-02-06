import pytest
from jose import jwt
from app import schemas
from app.config import settings


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
    login_res = schemas.Token(**res.json())

    # verify token
    payload = jwt.decode(login_res.access_token, key = settings.secret_key, algorithms = [settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

# paramatrize all possible inputs this way
@pytest.mark.parametrize("email, password, status_code", [
        ('wrongemail@gmail.com', 'password123', 403),
        ('hello123@gmail.com', 'wrongpassword', 403),
        ('wrongemail@gmail.com', 'wrongpassword', 403),
        (None, 'password123', 422),
        ('hello123@gmail.com', None, 422)
    ])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login",
        data = {
            "username": email,
            "password": password
        })
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'

