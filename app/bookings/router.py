from datetime import date

from fastapi import APIRouter, Depends, Request
from fastapi_versioning import version

from app.bookings.dependencies import get_current_user
from app.bookings.service import BookingsService
from app.bookings.shemas import SBookings
from app.exceptions import (
    BookingsCannotFound,
    ProhibitedDeleteException,
    RoomCannotBeBooked, ErrorBookingService,
)
from app.tasks.tasks import send_email_conformation_booking
from app.users.models import User
from app.users.shemas import UserShortResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get('', response_model=list[SBookings])
@version(1)
async def get_bookings(user: User = Depends(get_current_user)):
    bookings = await BookingsService.get_bookings_user(user_id=user.id)
    if not bookings:
        raise BookingsCannotFound
    elif isinstance(bookings, ErrorBookingService):
        raise ErrorBookingService
    bookings_list = [dict(row) for row in bookings.mappings().all()]
    email = "ciezar@lary-lcc.click"
    send_email_conformation_booking.delay(bookings_list, email)
    return bookings_list


@router.get('/{bookings_id}')
def get_bookings2(bookings_id):
    pass


@router.post('/add')
@version(1)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: User = Depends(get_current_user)
):
    booking = await BookingsService.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    if isinstance(booking, ErrorBookingService):
        raise ErrorBookingService


@router.delete('/delete-{booking_id}', status_code=204)
@version(1)
async def delete_booking(
        booking_id: int,
        user: User = Depends(get_current_user)
):
    deleted_entry = await BookingsService.delete_one_entry(id=booking_id, user_id=user.id)
    if not deleted_entry:
        raise ProhibitedDeleteException
