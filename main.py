from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

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


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):

    return {"data": post}
