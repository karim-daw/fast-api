from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# connecting with database
# later we need to not hardcode database information
while True:
    try:
        conn = psycopg2.connect(
            host = 'localhost',
            database = 'fastapi',
            user = 'postgres',
            password = 'dceazqwsx1991P.',
            cursor_factory=RealDictCursor
            )
        curser = conn.cursor()
        print("Database conenction was successfull!")
        break
    except Exception as error:
        print("Connecting to Database failed")
        print("Error; ", error)
        time.sleep(2)


# for not just save posts to memeory
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]

def find_post(id):
    """ find post based on id"""
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    """given an id, finds index of given post"""
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 


# root end point
@app.get("/")
async def root():
    return {"message": "Hello World"}

# root end point
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()


    return {"data": posts}


# get all posts
@app.get("/posts")
def get_posts():
    # make sql query and fetch data from db with curser
    curser.execute("""SELECT * FROM posts """)
    posts = curser.fetchall()

    #print(posts)
    return {"data": posts}


# create post 
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    # sanitzing input so we are not vunerable to sql injections used %s
    curser.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published))
    
    # get returned value 
    new_post = curser.fetchone()
    
    # push changes to db
    conn.commit()

    return {"data": new_post}


# getting singular post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    
    # select post with specif id
    curser.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = curser.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    # delete post
    curser.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id)) )
    delete_post = curser.fetchone()
    conn.commit()

    if delete_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# updating a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    curser.execute(
        """UPDATE posts SET title = %s,content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title,post.content, post.published, str(id)))

    updated_posts = curser.fetchone()
    conn.commit()

    if updated_posts == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")

    return {'data': updated_posts}
