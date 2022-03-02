from sqlalchemy import ForeignKey, text, TIMESTAMP, Column, Integer, Boolean, String
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer,primary_key=True,nullable=False)
  title=Column(String,nullable=False)
  content=Column(String,nullable=False)
  published=Column(Boolean,server_default='True',nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
  user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
  user = relationship("Users")

class Users(Base):
  __tablename__="users"
  id = Column(Integer,primary_key=True,nullable=False)
  email = Column(String,nullable=False,unique=True)
  password = Column(String,nullable=False)
  created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class votes(Base):
  __tablename__ = "votes"

  user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
  post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
