from .. import models
from ..schemas import *
from ..utils import *
from fastapi import HTTPException, status, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)

@router.post('/',response_model=UserOut,status_code=status.HTTP_201_CREATED)
def CreateUser(user: UserCreate,db: Session = Depends(get_db)):
  user.password = hash(user.password)
  created_user = models.Users(**user.dict())
  db.add(created_user)
  db.commit()
  db.refresh(created_user)
  return created_user

@router.get("/{id}",response_model=UserOut)
def getUser(id:int,db: Session = Depends(get_db)):
  user = db.query(models.Users).filter(models.Users.id == id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
  return user