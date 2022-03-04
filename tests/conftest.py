from pydoc import cram
import alembic
import fastapi
from fastapi.testclient import TestClient
from app.database import get_db, Base
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from alembic import command
from app.ouath2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # connect_args={"check_same_thread": False}

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def overide_get_db():
#   db = TestingSessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()

# app.dependency_overrides[get_db] = overide_get_db

@pytest.fixture()
def session():
  Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()

@pytest.fixture()
def client(session):
  def overide_get_db():
    try:
      yield session
    finally:
      session.close()
  app.dependency_overrides[get_db] = overide_get_db
  # command.upgrade("head")
  #before the code runs
  yield TestClient(app)
  #after the code runs
  # command.downgrade("base")

@pytest.fixture
def test_user(client):
  user_data = {"email":"hello123@gmail.com","password":"password"}
  res = client.post("/users/",json=user_data)
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_data["password"]
  return new_user

@pytest.fixture
def test_user1(client):
  user_data = {"email":"hello1234@gmail.com","password":"password"}
  res = client.post("/users/",json=user_data)
  assert res.status_code == 201
  new_user = res.json()
  new_user['password'] = user_data["password"]
  return new_user

@pytest.fixture
def token(test_user):
  return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def authourized_client(client,token):
  client.headers = {
    **client.headers,
    "Authorization": f"Bearer {token}"
  }
  return client

@pytest.fixture
def test_posts(test_user,session,test_user1):
  posts_data = [{
    "title": "First title",
    "content": "Test Content1",
    "user_id": test_user["id"]
  },
  {
    "title": "Second title",
    "content": "Test Content2",
    "user_id": test_user["id"]
  },
  {
    "title": "Third title",
    "content": "Test Content3",
    "user_id": test_user["id"]
  },
  {
    "title": "fourth title",
    "content": "fourth Content3",
    "user_id": test_user1["id"]
  }]
  def create_post_model(post):
    return models.Post(**post)
  session.add_all(list(map(create_post_model,posts_data)))
  session.commit()
  res = session.query(models.Post).all()
  return res

