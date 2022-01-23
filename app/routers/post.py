from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Body, Depends
from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# get all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""):

    print(search)

    # only retrieve posts if it comes for current user
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #print(posts)
    return posts

# create post 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)): # dependancy forces logged in


    #print(current_user.id)
    # create new post from unpacking post.dict()
    new_post = models.Post(owner_id = current_user.id , **post.dict())

    # add post to db and commit 
    db.add(new_post)
    db.commit()

    # retrieve new post and store it back into variable new_post
    db.refresh(new_post)
    return new_post


# getting singular post
@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post


# deleting a post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist")
    
    # check if post owner is same as authenticated current user
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action")

    # worth reading about in doc under "session basics"
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating a post
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id:{id} does not exist")

    # check if post owner is same as authenticated current user
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not Authorized to perform requested action")

    # if post exists, use update() to update with post from user 
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
