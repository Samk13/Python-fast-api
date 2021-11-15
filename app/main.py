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
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        # TODO: move to config
        conn = connect(
            database="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor,
        )
        cur = conn.cursor()
        print("✨🎉Connected to database successfully ✨🎉")

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


@app.get("/test")
def test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    # SQL way of doing it
    # keep the comma after str(post_id) to avoid syntax error
    # cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    # post = cur.fetchone()

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    return {"data": post}


# Delete post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
    #             (str(post_id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (
    #         post.title,
    #         post.content,
    #         post.published,
    #         str(post_id),
    #     ),
    # )
    # updated_post = cur.fetchone()
    # conn.commit()
    updated_post_query = db.query(models.Post).filter(models.Post.id == post_id)
    updated_post = updated_post_query.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": updated_post_query.first()}
