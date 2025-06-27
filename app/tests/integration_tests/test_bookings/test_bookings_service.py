from datetime import datetime

import pytest

from app.bookings.service import BookingsService


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


@pytest.mark.parametrize(
    ['user_id', 'count_bookings'],
    [
        (1, 2),
        (2, 1),
     ]
)
async def test_get_and_delete_user_bookings(
        user_id: int,
        count_bookings: int
):
    user_bookings = await BookingsService.get_bookings_user(user_id=user_id)
    bookings_list = user_bookings.mappings().all()
    assert bookings_list
    assert bookings_list[0].user_id == user_id
    for booking in bookings_list:
        await BookingsService.delete_one_entry(user_id=booking.user_id)
    user_bookings = await BookingsService.get_bookings_user(user_id=user_id)
    bookings_list = [dict(row) for row in user_bookings.mappings().all()]
    assert len(bookings_list) == 0


