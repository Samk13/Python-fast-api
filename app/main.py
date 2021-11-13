from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine

models.Base.metadata.create_all(bind=engine)
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
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                (post.title, post.content, post.published))
    new_post = cur.fetchone()
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, response: Response):
    # keep the comma after str(post_id) to avoid syntax error
    cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post id {post_id} not found"
        )
    return {"data": post}


# Delete post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, response: Response):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                (str(post_id),))
    deleted_post = cur.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post id {post_id} not found"
        )
    return {"message": f"Post '{deleted_post['title']}' deleted successfully"}


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, str(post_id),))
    updated_post = cur.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post id {post_id} not found"
        )
    return {"data": updated_post}

    # post_dict = post.dict()
    # post_update = find_post(post_id)
    # if not post_update:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
    #     )
    # else:
    #     for key in post_update:
    #         if key not in post_dict:
    #             post_dict[key] = post_update[key]
    #         post_update[key] = post_dict[key]

    #     return {"data": post_update}
