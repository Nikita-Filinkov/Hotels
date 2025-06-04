import asyncio
from datetime import datetime
import json
from fastapi.testclient import TestClient
from httpx import AsyncClient

import pytest
from sqlalchemy import insert

from app.database import Base, async_session_maker, engine
from app.config import settings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users
from app.bookings.models import Bookings
from app.main import app as fastapi_app
import os
os.environ["MODE"] = "TEST"


@pytest.fixture(autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"
    # Сначала удаляем все таблицы (если существуют)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        # Затем создаём заново
        await conn.run_sync(Base.metadata.create_all)

    def open_mok_json(model: str):
        with open(f"app/tests/mok_files/mock_{model}.json", encoding='utf-8') as file:
            return json.load(file)

    mock_values_hotels = open_mok_json("hotels")
    mock_values_rooms = open_mok_json("rooms")
    mock_values_users = open_mok_json("users")
    mock_values_bookings = open_mok_json("bookings")

    for booking in mock_values_bookings:
        # SQLAlchemy не принимает дату в текстовом формате, поэтому форматируем к datetime
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(mock_values_hotels)
        add_rooms = insert(Rooms).values(mock_values_rooms)
        add_users = insert(Users).values(mock_values_users)
        add_bookings = insert(Bookings).values(mock_values_bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


# Взято из документации к pytest-asyncio
# Создаем новый event loop для прогона тестов
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def asyncclient():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session