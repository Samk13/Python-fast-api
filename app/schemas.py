from pydantic import BaseModel
from datetime import datetime
from typing import List


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


# Response Schema is resposible for what keys are returned to the client
class PostResponse(PostBase):
    id: int
    created_at: datetime
    # add this config class to make SQLkalchemy convert the model to a dict or you will get an error

    class Config:
        orm_mode = True
