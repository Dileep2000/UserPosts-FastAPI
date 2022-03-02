from this import d
from fastapi import FastAPI,Depends, APIRouter, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models
from .. import utils
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import *
from .. import ouath2


router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(userCreds: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
  # usercreds - username and password
  user = db.query(models.Users).filter(models.Users.email == userCreds.username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
  if not utils.verify(userCreds.password,user.password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
  # Create token
  access_token = ouath2.create_access_token(data= {"user_id": user.id})
  #return Token
  return {"access_token": access_token, "token_type":"bearer"}
