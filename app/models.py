from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    # table name
    __tablename__ = "posts"

    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_defualt='TRUE',nullable=False)


