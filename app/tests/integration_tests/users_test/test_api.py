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

@pytest.mark.parametrize(['email', 'password', 'status_code'], [
    ('t@t.com', 't', 200),
    ('test@test.com', 'w', 409),
    ('q@q.com', 'q', 200),
    ('tt.com', 't', 422),
])
async def test_register_user(email, password, status_code, asyncclient: AsyncClient):
    response = await asyncclient.post("/auth/register", json={"email": email, "password": password})
    assert response.status_code == status_code


@pytest.mark.parametrize(
    [
        'email', 'password', 'status_code'
    ],
    [
        ('test@test.com', 'test', 200),
        ('artem@example.com', 'artem', 200),
        ('wrong@wrong.com', 'wrong', 401),
    ]
)
async def test_logging_user(email, password, status_code, asyncclient: AsyncClient):
    response = await asyncclient.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == status_code
