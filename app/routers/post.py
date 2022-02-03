from sqlalchemy import func
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.params import Body, Depends
from typing import List, Optional
from sqlalchemy import desc

# define router endpoint and documentaition tags
router = APIRouter( prefix="/posts", tags=['Posts'] )

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,skip: int = 0, search: Optional[str] = ""):

    """returns all posts given a post limit count, amoutn of posts to skip, and search string"""

    # only retrieve posts if it comes for current user
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).order_by(
                desc(models.Post.created_at)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
    #         models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)): # dependancy forces logged in

    """creates new post given a post schema, db dependancy and that current user is logged in"""

    # create new post from unpacking post.dict()
    new_post = models.Post(owner_id = current_user.id , **post.dict())

    # add post to db and commit 
    db.add(new_post)
    db.commit()

    # retrieve new post and store it back into variable new_post
    db.refresh(new_post)
    return new_post


# getting singular post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    """returns post given id, db dependancy and that current user is logged in"""

    # retrieve first post with given id, otherwise raise 404
    #post = db.query(models.Post).filter(models.Post.id == id).first()


    post = db.query(models.Post,
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    """deletes post given id, db dependancy and that current user is logged in"""

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
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    """updates post given an id, a PostCreate Schema and db dependancy"""
    
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
