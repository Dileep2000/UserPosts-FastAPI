from .. import models
from ..schemas import *
from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional
from .. import ouath2

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)

@router.get("/",response_model=List[PostOut])
async def get_posts(db: Session = Depends(get_db),user_id: int = Depends(ouath2.get_current_user),limit: int = 10,skip: int = 0, search: Optional[str] = ''):
  # cursor.execute("""SELECT * FROM "Posts";""")
  # my_posts = cursor.fetchall()
  # my_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  my_posts = db.query(models.Post,func.count(models.votes.post_id).label("votes")).join(models.votes, models.Post.id == models.votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  return my_posts

# @app.post("/postswithBody")
# async def createPosts(payload: dict = Body(...)):
#   print(payload)
#   return {"Message": f"new Post title: {payload['title']}, content: {payload['content']}"}

@router.post("/",response_model=ReturnPost)#,status_code=status.HTTP_404_NOT_FOUND)
async def create_Posts(payload: PostModel,db: Session = Depends(get_db), user: int = Depends(ouath2.get_current_user)):
  # id = randrange(2,10000000000000)
  # post_dict = payload.dict()
  # post_dict["id"] = id
  # posts.append(post_dict)

  # cursor.execute("""INSERT INTO "Posts" ("title","content","published") VALUES (%s,%s,%s) RETURNING *""",(payload.title,payload.content,payload.published))
  # created_post =  cursor.fetchone()
  # conn.commit()
  created_post =  models.Post(user_id = user.id,**payload.dict())#(title=payload.title,content=payload.content,published=payload.published)
  db.add(created_post)
  db.commit()
  db.refresh(created_post)
  return created_post

@router.get("/latest",response_model=PostOut)
def get_latest(db: Session = Depends(get_db),user_id: int = Depends(ouath2.get_current_user)):
  post = db.query(models.Post,func.count(models.votes.post_id).label("votes")).join(models.votes, models.Post.id == models.votes.post_id, isouter=True).group_by(models.Post.id).order_by('created_at').limit(1)
  return post

@router.get("/{id}",response_model=PostOut)
def get_post(id: int,response: Response,db: Session = Depends(get_db),user_id: int = Depends(ouath2.get_current_user)):
  # post = db.query(models.Post).filter(models.Post.id == id).first()
  post = db.query(models.Post,func.count(models.votes.post_id).label("votes")).join(models.votes, models.Post.id == models.votes.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
  # cursor.execute('''SELECT * FROM "Posts" WHERE id= %s''',(str(id)))
  # post = cursor.fetchone()
  # print(posts)
  # post = getfilteredpost(int(id))
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {id} was not found")
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id: {id} was not found"}
  return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete(id:int,db: Session = Depends(get_db),user: int = Depends(ouath2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id == id)
  # cursor.execute("""DELETE FROM "Posts" where id=%s RETURNING *;""",(str(id)))
  # deleted_post = cursor.fetchone()
  # conn.commit()
  deleted_post = post.first()
  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
  if deleted_post.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User is not allowed to delete this post")
  post.delete(synchronize_session=False)
  db.commit()
  # deleted_post=posts.pop(find_post_index(int(id)))
  # return {"message":f"deleted id:{id} of data {deleted_post}"}
  return {"deleted_post":"Deleted successfully"}

@router.put("/{id}",response_model=ReturnPost)
def update_post(id:int, post: PostModel,db: Session = Depends(get_db),user: int = Depends(ouath2.get_current_user)):
  post_query = db.query(models.Post).filter(models.Post.id == id)
  
  # cursor.execute("""UPDATE "Posts" SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
  # updated_post = cursor.fetchone()
  # conn.commit()
  
  if post_query.first() == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id: {id} was not found")
  if post_query.user_id != user.id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User is not allowed to Update this post")

  post_query.update(post.dict(),synchronize_session=False)#({'title':post.title,'content':post.content,'published':post.published},synchronize_session=False)
  db.commit()
  # post_dict = post.dict()
  # post_dict['id'] = id
  # posts[find_post_index(id)] = post_dict
  return post_query.first()