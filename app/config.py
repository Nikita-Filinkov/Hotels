import os
from base64 import b64encode
from secrets import token_bytes
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DATABASE_URL: Optional[str] = None

    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    TEST_DB_HOST: str = "db"
    TEST_DB_PORT: int = 5432
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str

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
    if settings.DATABASE_URL:
        return settings.DATABASE_URL
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


def test_get_db_url():
    return (f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@"
            f"{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}")