from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# import all routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# root end point
@app.get("/")
async def root():
    return {"message": "Hello World"}

