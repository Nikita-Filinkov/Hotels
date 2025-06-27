from __future__ import annotations

import asyncio
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter, parse_obj_as

from app.bookings.dependencies import get_current_user
from app.exceptions import WrongDatesRegistrationsException
from app.hotels.service import HotelsService
from app.hotels.shemas import HotelsArgs, SHotels, SOneHotels
from app.users.models import Users

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
# @cache(expire=60)
async def hotels_on_location(
        locations: str,
        date_from: date = Query(description=f"Например: 2023-05-15"),
        date_to: date = Query(description=f"Например: 2023-06-30")
):
    # await asyncio.sleep(3)
    free_hotels = await HotelsService.get_hotels_on_location(
        locations=locations,
        date_from=date_from,
        date_to=date_to
    )
    if date_from >= date_to or date_to - date_from > timedelta(days=30):
        raise WrongDatesRegistrationsException

    result = [dict(TypeAdapter(SHotels).validate_python(hotel_data)) for hotel_data in free_hotels]
    # for hotel_data in free_hotels:
    #     result.append(dict(TypeAdapter(SHotels).validate_python(hotel_data)))

    # return free_hotels
    return result

