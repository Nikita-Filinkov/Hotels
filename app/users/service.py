from sqlalchemy import select

from app.database import async_session_maker
from app.service.base import BaseService
from app.users.models import Users
from app.users.shemas import UserShortResponse


class UsersService(BaseService):
    model = Users

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model.id, cls.model.email).where(cls.model.id == model_id)
            result = await session.execute(query)
            if row := result.first():
                return UserShortResponse(id=row[0], email=row[1])
            return None


