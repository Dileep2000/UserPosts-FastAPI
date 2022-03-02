from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas, models, config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SecretKey
# Algo -HS256
# Expiration Time
SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minute

def create_access_token(data: dict):
  to_encode = data.copy()

  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str, credentail_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    id = payload.get('user_id')
    if id is None:
      raise credentail_exception
    token_data = schemas.TokenData(id=id)
  except JWTError:
    raise credentail_exception
  return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"Could not validate Credentials",headers={"WWW-Authenticate":"Bearer"})
  
  token = verify_access_token(token=token,credentail_exception=credential_exception)
  user = db.query(models.Users).filter(models.Users.id == token.id).first()
  return user
