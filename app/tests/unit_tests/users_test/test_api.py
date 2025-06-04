import pytest
from httpx import AsyncClient


# @pytest.mark.asyncio
# async def test_database_connection():
#     from app.database import async_session_maker
#     from sqlalchemy import text
#
#     async with async_session_maker() as session:
#         result = await session.execute(text("SELECT 1"))
#         assert result.scalar() == 1



@pytest.mark.asyncio
async def test_register_user(asyncclient: AsyncClient):
    response = await asyncclient.post("/auth/register", json={"email": 't@t.com', "password": "t"})
    assert response.status_code == 200
