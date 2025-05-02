from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends

from app.hotels.shemas import HotelsArgs, SOneHotels, SHotels
from app.hotels.service import HotelsService
from app.users.models import Users
from app.bookings.dependencies import get_current_user

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)
# user: Users = Depends(get_current_user),
# hotel_args: HotelsArgs = Depends()


@router.get('/id/{hotel_id}', response_model=list[SOneHotels])
async def get_one_hotel(hotel_id: int):
    hotel = await HotelsService.find_by_id(model_id=hotel_id)
    return hotel


@router.get('/{locations}', response_model=list[SHotels])
async def hotels_on_location(
        locations: str,
        date_from: date,
        date_to: date
):
    free_hotels = await HotelsService.get_hotels_on_location(
        locations=locations,
        date_from=date_from,
        date_to=date_to
    )
    return free_hotels
