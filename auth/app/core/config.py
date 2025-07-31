# app/core/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_ENV: str = "dev"
    TZ: str = "Europe/Paris"
    ALLOW_ORIGINS: list[str] = ["*"]

    # Database
    SQLALCHEMY_DATABASE_URI: str = ""

    # Auth
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 0
    SECURE_COOKIE: bool = False


settings = Settings()
