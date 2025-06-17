from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.service.base import BaseService

from sqlalchemy import update, select, and_, or_, func, CTE


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def _get_booked_rooms(cls, date_from, date_to):
        """ WITH booked_rooms AS (
            SELECT *  FROM bookings
            WHERE
            (date_from <= '2023-05-15' AND date_to >= '2023-05-15') OR
            (date_from >= '2023-05-15' AND date_from <= '2023-06-30')
    )"""

        booked_rooms: CTE = select(Bookings.room_id).where(
            or_(
                and_(
                    Bookings.date_from <= date_from,
                    Bookings.date_to >= date_from
                ),
                and_(
                    Bookings.date_from >= date_from,
                    Bookings.date_from <= date_to
                )

            )
        ).cte("booked_rooms")
        return booked_rooms

    @classmethod
    async def update_one_entry(cls, hotel_id, **data):
        async with async_session_maker() as session:
            query = update(cls.model).filter_by(id=hotel_id).values(**data)
            result = await session.execute(query).returning(cls.model)
            await session.commit()
            return result.rowcount

    @classmethod
    async def get_hotels_on_location(cls, locations, date_from, date_to):
        """
            WITH booked_rooms AS (
            SELECT *  FROM bookings
            WHERE
            (date_from <= '2023-05-15' AND date_to >= '2023-05-15') OR
            (date_from >= '2023-05-15' AND date_from <= '2023-06-30')
    )


            SELECT
            hotels.id,
            hotels.name,
            hotels.locations,
            hotels.services,
            hotels.rooms_quantity,
            hotels.image_id,
            (hotels.rooms_quantity - COUNT(booked_rooms)) AS free_rooms
            FROM hotels
            JOIN rooms ON hotels.id = rooms.hotel_id
            JOIN booked_rooms ON rooms.id = booked_rooms.room_id
            WHERE hotels.locations = 'ул. Центральная, 1'
            GROUP BY hotels.id, booked_rooms.room_id
            HAVING hotels.rooms_quantity - COUNT(booked_rooms) > 0
        """
        async with async_session_maker() as session:
            booked_rooms: CTE = await cls._get_booked_rooms(date_from, date_to)

            query = select(
                cls.model.__table__,
                (
                    cls.model.rooms_quantity - func.count(booked_rooms.c.room_id)).label("free_rooms")
                ).select_from(
                cls.model
                ).join(
                Rooms, cls.model.id == Rooms.hotel_id
                ).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(
                cls.model.locations == locations
                ).group_by(
                cls.model.id
                ).having(
                cls.model.rooms_quantity - func.count(booked_rooms.c.room_id) > 0
                )

            result = await session.execute(query)
            return result.mappings().all()


    # @classmethod
    # async def get_hotels_on_location(cls, locations, date_from, date_to):
    #     async with async_session_maker() as session:
    #         query = select(cls.model).where(cls.model.locations == locations)
    #         result = await session.execute(query)
    #         hotels = result.scalars().all()
    #
    #         if not hotels:
    #             return []

    #         return hotels
