import json
import pytest
from app import schemas

def test_get_posts(authourized_client,test_posts):
  res = authourized_client.get("/posts/")
  def valiadtePost(post):
    return schemas.PostOut(**post)
  posts_list = list(map(valiadtePost,res.json()))
  assert len(res.json()) == len(test_posts)
  assert res.status_code == 200

def test_unauthorized_get_posts(client,test_posts):
  res = client.get("/posts/")
  assert res.status_code == 401

def test_unauthorized_get_one_post(client,test_posts):
  res = client.get(f"/posts/{test_posts[0].id}")
  assert res.status_code == 401

def test_unauthorized_get_one_post_does_not_exist(authourized_client,test_posts):
  res = authourized_client.get(f"/posts/888888")
  assert res.status_code == 404

def test_get_one_post(authourized_client,test_posts):
  res = authourized_client.get(f"/posts/{test_posts[0].id}")
  post = schemas.PostOut(**res.json())
  assert res.status_code == 200
  assert post.Post.id == test_posts[0].id
  assert post.Post.title == test_posts[0].title
  assert post.Post.content == test_posts[0].content
  assert post.Post.published == test_posts[0].published

@pytest.mark.parametrize("title, content, published",[
  ("New title","New Content",True),
  ("New title1","New Content1",False),
  ("New title2","New Content2",True)
])
def test_create_post(authourized_client,test_posts, test_user,title,content,published):
  res = authourized_client.post("/posts/",json={"title":title,"content":content,"published":published})
  created_post = schemas.ReturnPost(**res.json())
  assert res.status_code == 200
  assert created_post.title == title
  assert created_post.content == content
  assert created_post.published == published
  assert created_post.user_id == test_user["id"]

def test_unauthorized_create_post(client,test_posts, test_user):
  res = client.post("/posts/",json={"title":"title","content":"content","published":"published"})
  assert res.status_code == 401

def test_create_post_default(authourized_client,test_posts,test_user):
  res = authourized_client.post("/posts/",json={"title":"title","content":"content"})
  created_post = schemas.ReturnPost(**res.json())
  assert res.status_code == 200
  assert created_post.title == "title"
  assert created_post.content == "content"
  assert created_post.published == True
  assert created_post.user_id == test_user["id"]

def test_unauthourized_delete_post(client,test_posts,test_user):
  res = client.delete(f"/posts/{test_posts[0].id}")
  assert res.status_code == 401

def test_authourized_delete_post(authourized_client,test_posts,test_user):
  res = authourized_client.delete(f"/posts/{test_posts[0].id}")
  posts = authourized_client.get("/posts/")
  assert res.status_code == 204
  assert len(posts.json()) == len(test_posts) - 1

def test_delete_non_exist(authourized_client,test_posts):
  res = authourized_client.delete("/posts/80000")
  assert res.status_code == 404

def test_delete_other_user_post(authourized_client,test_posts,test_user1):
  res = authourized_client.delete(f"/posts/{test_posts[3].id}")
  assert res.status_code == 403

def test_authorized_update_post(authourized_client,test_posts,test_user):
  data = {
    "title": "updated title",
    "content": "updated content",
    "published": False,
    "id": test_posts[0].id
  }
  res = authourized_client.put(f"/posts/{test_posts[0].id}",json=data)
  updated_post = schemas.ReturnPost(**res.json())
  assert res.status_code == 200
  assert updated_post.title == data["title"]
  assert updated_post.content == data["content"]
  assert updated_post.published == data["published"]

def test_unauthorized_update_post(client,test_posts,test_user):
  data = {
    "title": "updated title",
    "content": "updated content",
    "published": False,
    "id": test_posts[0].id
  }
  res = client.put(f"/posts/{test_posts[0].id}",json=data)
  assert res.status_code == 401

def test_updated_other_user_post(authourized_client,test_posts,test_user,test_user1):
  data = {
    "title": "updated title",
    "content": "updated content",
    "published": False,
    "id": test_posts[3].id
  }
  res = authourized_client.put(f"/posts/{test_posts[3].id}",json=data)
  assert res.status_code == 403

def test_update_post_non_exist(authourized_client,test_posts,test_user):
  data = {
    "title": "updated title",
    "content": "updated content",
    "published": False,
    "id": test_posts[3].id
  }
  res = authourized_client.put(f"/posts/80000",json=data)
  assert res.status_code == 404
