from pydantic import BaseModel

# Pydantic model, it will ensure that the data is valid for the schema
# you can create differnet mdoels for different requests so that for more flexibility

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass
