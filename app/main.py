from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# use uvicorn main:app to start production server
# use uvicorn main:app --reload to start development server

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# cors policies
origins = [
    "http://localhost:8080",
    "*"
    ] # declare which origins can access api * would mean public api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 
    allow_headers=["*"],
)

# import all routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# root end point
@app.get("/")
async def root():
    return {"message": "Hello World, im Karim!!!"}

