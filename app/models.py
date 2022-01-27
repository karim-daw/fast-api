from tkinter import CASCADE
from sqlalchemy.sql.expression import text, true
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy import Column, ForeignKey, ForeignKeyConstraint, Integer, String, Boolean
from sqlalchemy.orm import relationship

# these is sqlalchemy model

"""Post data model"""
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete=CASCADE), nullable=False)
    
    # create a owner property that creates a relationship to User class
    owner = relationship("User")

"""User data model"""
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


"""Vote data model"""
class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete = CASCADE), primary_key =True)
    post_id = Column(Integer, ForeignKey( "posts.id", ondelete= CASCADE), primary_key=True)
  

