from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import IntEnum

from app import database

class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserOut(BaseModel):
  id: int
  email: str
  created_at: datetime
  class Config:
    orm_mode = True

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class PostModel(BaseModel):
  title: str
  content: str
  published: bool = True
  # rating: Optional[int] = None

class CreatePost(PostModel):
  pass

class ReturnPost(PostModel):
  id: int
  user_id: int
  created_at: datetime
  user: UserOut
  class Config:
    orm_mode = True

class PostOut(BaseModel):
  Post: ReturnPost
  votes: int
  class Config:
    orm_mode = True


class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: Optional[str] = None

class IntEnum(IntEnum):
  zero = 0
  one = 1

class Vote(BaseModel):
  post_id: int
  dir: IntEnum