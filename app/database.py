from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:dceazqwsx1991P.@localhost/fastapi"

# use conenction string in engine 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependancy
# The session object talks to databse, we get a session for the database everytime we get request
# more efficient, we keep calling this function everytime we get a request to api end points
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()