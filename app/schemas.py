from pydantic import BaseModel


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
