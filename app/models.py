from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Post(Base):
    # table name
    __tablename__ = "post"

    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)

