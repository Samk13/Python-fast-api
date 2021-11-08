from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        # TODO: move to config
        conn = connect(
            database="fast-api",
            user="admin",
            password="admin",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        print("✨🎉Connected to database succsesfully ✨🎉")

        cur.execute("SELECT * FROM posts")
        my_posts = cur.fetchall()
        break
    except Exception as e:
        print("😐 Error:", e)
        print("Trying to connect to database again in 5 seconds...")
        time.sleep(5)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}


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
    else:
        for i in range(5):
            for j in range(i):
                print("* ", end="")
            print("")
        return {"data": result}


# Delete post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, response: Response):
    result = find_post(post_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    else:
        my_posts.remove(result)
        return {"message": f"Post '{result['title']}' deleted successfully"}
        # return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    post_dict = post.dict()
    post_update = find_post(post_id)
    if not post_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    else:
        for key in post_update:
            if key not in post_dict:
                post_dict[key] = post_update[key]
            post_update[key] = post_dict[key]

        return {"data": post_update}
