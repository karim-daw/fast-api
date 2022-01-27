from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# Pydantic model, it will ensure that the data is valid for the schema
# you can create differnet mdoels for different requests so that for more flexibility

"""User data classes"""
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # tells pydantic to ignore the fact that it isnt a dict
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


"""Post data classes"""
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    # return pydantic model called UserOut to complete db relationship
    owner: UserOut

    # tells pydantic to ignore the fact that it isnt a dict
    class Config:
        orm_mode = True


"""Token data class"""
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


""" Vote data class"""
class Vote(BaseModel):
    post_id: int

    # restricting to only 0 and 1
    dir: conint(gt = 0, le=1)