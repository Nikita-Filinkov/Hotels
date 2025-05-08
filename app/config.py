import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from secrets import token_bytes
from base64 import b64encode


class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    SECRET_KEY: str = b64encode(token_bytes(32)).decode()
    ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_EMAIL: str
    SMTP_PASS: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra='ignore'
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")