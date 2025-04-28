from datetime import date

from sqlalchemy import select, and_, or_, func, insert
from sqlalchemy.sql.expression import CTE

from app.bookings.models import Bookings
from app.database import engine, async_session_maker
from app.hotels.models import Rooms
from app.service.base import BaseService


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date,
    ):

        """

        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from <= '2023-05-15' AND date_to >= '2023-05-15') OR
            (date_from >= '2023-05-15' AND date_from <= '2023-06-30')
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON rooms.id = booked_rooms.room_id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity

        """
        async with async_session_maker() as session:
            booked_rooms: CTE = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
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
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True
            ).where(
                Rooms.id == 1
            ).group_by(
                Rooms.quantity, Rooms.id
            )

            print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            print(rooms_left)

            if rooms_left > 0:
                get_price = select(Rooms.price).where(Rooms.id == room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,

                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                new_booking = new_booking.scalar()
                return new_booking
            else:
                return None
