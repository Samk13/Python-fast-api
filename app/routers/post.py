# -*- coding: utf-8 -*-
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, oauth2
from typing import List, Optional

router = APIRouter(prefix="/posts", tags=["posts"])
Post = schemas.Post
CreatePost = schemas.CreatePost
UpdatePost = schemas.PostUpdate


@router.get("/", response_model=List[schemas.PostResponseVotes])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    # SQL way of doing it
    # cur.execute("""SELECT * FROM posts""")
    # posts = cur.fetchall()
    # https://youtu.be/0sOvCWFmrtA?t=37238 - explanation of the query
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: CreatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # SQL way of doing it
    # cur.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published),
    # )
    # new_post = cur.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# @router.get("/{post_id}")
@router.get("/{post_id}", response_model=schemas.PostResponseVotes)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # SQL way of doing it
    # keep the comma after str(post_id) to avoid syntax error
    # cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    # post = cur.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == post_id).first()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == post_id)
        .first()
    )
    # post = (
    #     db.query(
    #         models.Post,
    #         func.count(models.Vote.post_id)
    #         .label("votes")
    #     )
    #     .join(
    #         models.Vote,
    #         models.Vote.post_id == models.Post.id,
    #         isouter=True
    #     )
    #     .group_by(models.Post.id)
    #     .filter(models.Post.id == post_id)
    #     .first()
    # )
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id {post_id} not found"
        )
    if post.Post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform  requested action",
        )
    return post


# Delete post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform  requested action",
        )
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{post_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PostResponse,
)
def update_post(
    post_id: int,
    post: UpdatePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
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
    if updated_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform  requested action",
        )
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post_query.first()
