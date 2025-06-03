import pytest


@pytest.mark.asyncio
async def test_database_connection():
    from app.database import async_session_maker
    from sqlalchemy import text

    async with async_session_maker() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
