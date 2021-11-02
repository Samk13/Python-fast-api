from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


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
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new_post": f"the new post is {payload['id']} with title {payload['title']}"}
