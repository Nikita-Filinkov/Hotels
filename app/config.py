import os
from base64 import b64encode
from secrets import token_bytes
from typing import Literal

from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    DATABASE_URL: str | None = None

    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASS: str = ""

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

    # model_config = SettingsConfigDict(
    #     env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
    #     extra='ignore'
    # )

    @property
    def database_url(self):
        if self.MODE == "PROD":
            return f"postgresql+asyncpg://{self.DB_USER}:{quote(self.DB_PASS)}@{self.DB_HOST}/{self.DB_NAME}"
        elif self.MODE == "TEST":
            return f"postgresql+asyncpg://{self.TEST_DB_USER}:{quote(self.TEST_DB_PASS)}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        return f"postgresql+asyncpg://{self.DB_USER}:{quote(self.DB_PASS)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()


