import time
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
Post = schemas.Post
CreatePost = schemas.CreatePost
UpdatePost = schemas.PostUpdate
Res = schemas.PostResponse

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


def find_post(id):
    for post in my_posts:
        if int(post["id"]) == int(id):
            return post
    return None


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts", response_model=List[Res])
def get_posts(db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Res)
def create_posts(post: CreatePost, db: Session = Depends(get_db)):
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
    return new_post


@app.get("/posts/{post_id}", response_model=Res)
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
    return post


# Delete post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
    #             (str(post_id),))
    # deleted_post = cur.fetchone()
    # conn.commit()
    deleted_post = db.query(models.Post).filter(
        models.Post.id == post_id).first()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Res)
def update_post(post_id: int, post: UpdatePost, db: Session = Depends(get_db)):
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
    updated_post_query = db.query(
        models.Post).filter(models.Post.id == post_id)
    updated_post = updated_post_query.first()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()


# User CRUD

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if new_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Email already registered",
        )
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
