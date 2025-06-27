from sqlalchemy import update

from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def update_one_entry(cls, hotel_id, name, **data):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(hotel_id=hotel_id, name=name).values(**data)
            result = await session.execute(query).returning(cls.model)
            await session.commit()
            return result.rowcount


