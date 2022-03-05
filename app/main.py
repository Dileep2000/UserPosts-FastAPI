from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from . import models
# from .database import engine
from .routes import posts, users, auth, votes

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# posts = [{"title":"title1","content":"content of title1","id":1}, {"title":"favouritr food","content":"pizza","id":2}]

# def getfilteredpost(id):
#   for post in posts:
#     if post['id'] == id:
#       return post

# def find_post_index(id):
#   for index,post in enumerate(posts):
#     if post['id']==id:
#       return index

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(votes.router)

@app.get("/")
async def root():
  return {'message':"Welcome to my API!!", "Creater":"Dileep","Contact":"e.dileep2000@gmail.com","Usage":"Go to /docs from the link where you are!","Usage":"To see how to use the api wait for some time to work on it"}
