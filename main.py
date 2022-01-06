from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def get_create_posts(post: Post):

    # convert to dict and add random id
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)

    my_posts.append(post_dict)
    return {"data": post}

# getting singular post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index in the array that has required ID
    index = find_index_post(id)
    my_posts.pop(index)
    return {'message': "post was succussfully deleted"}
