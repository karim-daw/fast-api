from pydantic import BaseSettings

# handling environement variables

class Settings(BaseSettings):
    """This class handles are the environment variables defined in
    .env file, this is a pydantic model which will verify all variables"""
    
    database_hostname: str 
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"



settings = Settings()