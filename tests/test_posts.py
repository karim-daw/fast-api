from itsdangerous import json
from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    posts_list = list(map(lambda post: schemas.PostOut(**post), res.json()))
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title 1", "awesome new content 1", True),
    ("i love pizza", "espeically pepporoni", False),
    ("i dont like shrimp", "except tiger shrimp", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    input_json={"title": title, "content": content, "published": published}
    res = authorized_client.post(f"/posts/",json=input_json)

    created_post = schemas.Post(**res.json())
    assert res.status_code ==201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    input_json={"title": "random title", "content": "random content"}
    res = authorized_client.post(f"/posts/",json=input_json)

    created_post = schemas.Post(**res.json())
    assert res.status_code ==201
    assert created_post.title == "random title"
    assert created_post.content == "random content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    input_json={"title": "random title", "content": "random content"}
    res = client.post(f"/posts/",json=input_json)
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/80000000")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client,test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client,test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.id == data["id"]
