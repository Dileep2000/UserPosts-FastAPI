from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..ouath2 import get_current_user
from .. import schemas, models

router = APIRouter(tags=["votes"],prefix="/vote")

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {vote.post_id} is not found")
  voted = db.query(models.votes).filter(models.votes.post_id == vote.post_id,models.votes.user_id == user.id)
  if vote.dir == 1:
    if voted.first():
      raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"Post {vote.post_id} is already voted by user {user.id}")
    else:
      new_vote = models.votes(post_id=vote.post_id,user_id=user.id)
      db.add(new_vote)
      db.commit()
      return {"message":"Successfully added vote"}
  else:
    if voted.first():
      voted.delete(synchronize_session=False)
      db.commit()
      return {"message":"successfully removed vote"}
    else:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {vote.post_id} is not voted by user {user.id}")      
