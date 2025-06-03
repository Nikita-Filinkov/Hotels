from __future__ import annotations

import asyncio
from datetime import date
from pydantic import parse_obj_as

from fastapi import APIRouter, Depends, Query

from fastapi_cache.decorator import cache

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


@router.get('/id/{hotel_id}', response_model=SOneHotels)
async def get_one_hotel(hotel_id: int):
    hotel = await HotelsService.find_by_id(model_id=hotel_id)
    return hotel


@router.get('/{locations}', response_model=list[SHotels])
@cache(expire=60)
async def hotels_on_location(
        locations: str,
        date_from: date = Query(description=f"Например: 2023-05-15"),
        date_to: date = Query(description=f"Например: 2023-06-30")
):
    await asyncio.sleep(3)
    free_hotels = await HotelsService.get_hotels_on_location(
        locations=locations,
        date_from=date_from,
        date_to=date_to
    )
    print(type(free_hotels[0]))
    free_hotels = parse_obj_as(list[SHotels], free_hotels)
    print(type(free_hotels[0]))
    return free_hotels
