from pydantic import BaseModel
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
