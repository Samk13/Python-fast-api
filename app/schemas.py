from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):
    pass


class CreatePost(PostBase):
    pass


class PostUpdate(PostBase):
    published: bool


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Response Schema is resposible for what keys are returned to the client


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # add this config class to make SQLkalchemy convert the model to a dict or you will get an error

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
