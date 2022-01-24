from passlib.context import CryptContext

# create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password: str):
    """returns hashed password"""
    return pwd_context.hash(password)

# verify password
def verify(plain_password, hashed_password):
    """returns true if password and hashed password equal eachother"""
    return pwd_context.verify(plain_password, hashed_password)