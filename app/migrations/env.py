import asyncio
import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import settings

sys.path.insert(0, dirname(dirname(dirname(abspath(__file__)))))

from app.bookings.models import Bookings # noqa
from app.database import Base
from app.hotels.models import Hotels # noqa
from app.hotels.rooms.models import Rooms # noqa
from app.users.models import User # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
load_dotenv()

config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автогенерации миграций
target_metadata = Base.metadata


def prepare_db_url(db_url: str) -> str:
    """Добавляет параметры SSL для Production"""
    if settings.MODE == "PROD" and "ssl=require" not in db_url.lower():
        return f"{db_url}?ssl=require" if "?" not in db_url else f"{db_url}&ssl=require"
    return db_url


def run_migrations_offline() -> None:
    """Запуск миграций в offline-режиме (без подключения к БД)"""
    url = prepare_db_url(settings.database_url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Асинхронное выполнение миграций"""
    db_url = prepare_db_url(settings.database_url)
    engine = create_async_engine(
        db_url,
        poolclass=NullPool,
        connect_args={"timeout": 30} if settings.MODE == "PROD" else {}
    )

    async with engine.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
                compare_server_default=True
            )
        )
        await connection.run_sync(lambda sync_conn: context.run_migrations())


def run_migrations_online() -> None:
    """Запуск миграций в online-режиме"""
    asyncio.run(run_async_migrations())

# Выбор режима выполнения миграций
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()