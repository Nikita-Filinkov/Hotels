from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


def get_db_params():
    params = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_pre_ping": True
    }

    if settings.MODE == "TEST":
        params["poolclass"] = NullPool
    elif settings.MODE == "PROD":
        params["connect_args"] = {"ssl": "require", "timeout": 30}

    return params


engine = create_async_engine(
    settings.database_url,
    **get_db_params()
)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

