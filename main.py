from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts")
def get_posts():
    return [
        {"id": 1, "title": "Hello World"},
        {"id": 2, "title": "Hello Galaxy"},
    ]


@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post)
    return {"new_post": f"the new post is {new_post.title, new_post.content}"}
