from typing import Dict
from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET KEY
# Algorythm
# Expiration time

# using - openssl rand -hex 32
SECRET_KEY = "481495a86cf3e0ee73cb7abcec6cc87c233c6a26e5ed109606f9646c15f7b09e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPERIRATION_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPERIRATION_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)