from fastapi import APIRouter, Request, Depends

from app.bookings.dependencies import get_current_user
from app.bookings.service import BookingsService
from app.bookings.shemas import SBookings
from app.users.models import Users
from app.users.shemas import UserShortResponse

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookings]:
    return await BookingsService.get_all(user_id=user.id)


@router.get('/{bookings_id}')
def get_bookings2(bookings_id):
    pass


@router.post('/add')
async def add_booking(
        user: Users = Depends(get_current_user)
):
    await BookingsService.add()
