from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Text


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=True)
    created_date = Column(DateTime, default=func.now())
    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship(
    #     'Users', backref=backref('posts', lazy='dynamic'))

    # def __init__(self, title, content, user_id):
    #     self.title = title
    #     self.content = content
