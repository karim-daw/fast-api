from pydantic import BaseModel, EmailStr
from datetime import datetime

# Pydantic model, it will ensure that the data is valid for the schema
# you can create differnet mdoels for different requests so that for more flexibility

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    # tells pydantic to ignore the fact that it isnt a dict
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # tells pydantic to ignore the fact that it isnt a dict
    class Config:
        orm_mode = True