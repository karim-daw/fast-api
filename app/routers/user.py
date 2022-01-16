from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Body, Depends

router = APIRouter(
    prefix= "/users",
    tags=['Users']
)

# create user 
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # create hash of password - user.passowrd and update pydantic user.password model
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    
    # add post to db and commit 
    db.add(new_user)
    db.commit()

    # retrieve new post and store it back into variable new_post
    db.refresh(new_user)
    return new_user

# getting single user
@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    return user