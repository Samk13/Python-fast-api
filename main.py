from fastapi import FastAPI, Response, status, HTTPException
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


def error_message(message):
    return {"message": message}


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(10000000, 99999999)
    my_posts.append(post_dict)

    return {"data": post_dict}


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    result = find_post(post_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post id {post_id} not found",
            headers={"X-Error": "Post not found"},
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return error_message(f"Post with id:{post_id} not found")
    else:
        return {"data": result}
