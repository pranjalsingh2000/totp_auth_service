# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./totp.db"  # default for dev
    ENCRYPTION_KEY: str = "dbpassword"
    api_key: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields in the config

settings = Settings()
