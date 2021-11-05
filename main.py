from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {
        "title": "First post",
        "content": "This is my first post",
        "published": True,
        "rating": 5,
        "id": 123,
    },
    {
        "title": "Second post",
        "content": "This is my second post",
        "published": False,
        "rating": 4,
        "id": 456,
    },
]


def find_post(id):
    for post in my_posts:
        if int(post["id"]) == int(id):
            return post
    return None


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(10000000, 99999999)
    my_posts.append(post_dict)

    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if find_post(post_id) != None:
        return {"data": find_post(post_id)}
    else:
        return {"message": "Post not found"}
