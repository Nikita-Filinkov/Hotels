from app.bookings.service import BookingsService
from datetime import datetime


async def test_add_and_get_booking():
    date_from = datetime.strptime('2026-05-15', '%Y-%m-%d')
    date_to = datetime.strptime('2026-06-30', '%Y-%m-%d')
    new_booking = await BookingsService.add(
        user_id=2,
        room_id=2,
        date_from=date_from,
        date_to=date_to
    )
    booking = await BookingsService.find_one_or_none(
        user_id=2,
        room_id=2,
        date_from=date_from,
        date_to=date_to
    )
    assert new_booking
    assert new_booking.id == booking.id
