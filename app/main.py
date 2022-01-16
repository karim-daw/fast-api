from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body, Depends
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# import all routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# root end point
@app.get("/")
async def root():
    return {"message": "Hello World"}

