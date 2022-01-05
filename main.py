from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# for not just save posts to memeory
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def get_create_ports(post: Post):

    # convert to dict and add random id
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)

    my_posts.append(post_dict)
    return {"data": post}

# getting singular post
@app.get("/posts/{id}")
def get_post(id):
    post = find_post(int(id))
    return {"post_detail": post}

