from app.bookings.models import Bookings
from app.service.base import BaseService


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def add(cls):
        pass