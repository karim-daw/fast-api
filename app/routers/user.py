from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Body, Depends

# define router endpoint and documentaition tags
router = APIRouter( prefix= "/users", tags=['Users'] )

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    """Returns a new user given a UserCreate schema and a fastapi Database dependancy"""

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

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    """Returns an exisiting user given an id and fastapi Database dependancy"""
    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found")
    return user

"""@router.get("/me", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    
    user: _schemas.User = _fastapi.Depends(_services.get_current_user)
    return user

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)"""