from audioop import add
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from fastapi.params import Depends
from sqlalchemy.orm import Session



router = APIRouter( prefix= "/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user)):

    # check if user is trying to vote on a post that does not exit
    # query if post based on id first, if it doesnt exit throw exception
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f'Post with id: {vote.post_id} does not exist' )

    # if post exists, query db for vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)
    
    # getting first found vote from query and using that to check against vote direction
    # if vote direction set to 1, and an exisiting vote was found, that means a user is trying to vote twice, retun 409
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail = f'user {current_user.id} has already voted on post {vote.post_id}')

        # if no vote was found, create a new vote and add the new vote to the db
        new_vote = models.Vote(post_id= vote.post_id, user_id= current_user.id)
        db.add(new_vote)
        db.commit()

        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}


    