from pyexpat import model
from typing import Dict
import fastapi
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app import schemas
from sqlalchemy.orm import Session

# here you have to provide your login end point 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY
# Algorythm
# Expiration time

# using - openssl rand -hex 32
SECRET_KEY = "481495a86cf3e0ee73cb7abcec6cc87c233c6a26e5ed109606f9646c15f7b09e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPERIRATION_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPERIRATION_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not valiate credientials",
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credential_exception)

    # query database and return current user
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user