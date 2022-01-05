from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your post"}

@app.post("/posts")
def get_create_ports(new_post: Post):
    print(new_post)
    print(new_post.dict())
    return {"data": "this is your post"}

# title str, content str
