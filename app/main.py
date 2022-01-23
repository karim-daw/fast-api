from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth
from pydantic import BaseSettings
# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

# handling environement variables
class Settings(BaseSettings):
    database_password: str = "localhost"
    database_username: str = "postgres"
    secrect_key: str ="123iujasdiuj124"

settings = Settings()
print(settings.database_password)
print(settings.database_username)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# import all routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# root end point
@app.get("/")
async def root():
    return {"message": "Hello World"}

