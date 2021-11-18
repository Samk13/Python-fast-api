from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])
Res = schemas.PostResponse
Post = schemas.Post
CreatePost = schemas.CreatePost
UpdatePost = schemas.PostUpdate


@router.get("/", response_model=List[Res])
def get_posts(db: Session = Depends(get_db)):
    # SQL way of doing it
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Res)
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


@router.get("/{post_id}", response_model=Res)
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
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put(
    "/{post_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Res
)
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