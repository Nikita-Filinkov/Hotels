from __future__ import annotations

from fastapi import APIRouter, Depends

from app.hotels.shemas import HotelsArgs, SHotel
from app.hotels.service import HotelsService

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels']
)


@router.get('', response_model=list[SHotel])
async def get_hotels(
        hotel_args: HotelsArgs = Depends()
):
    filters = {}
    if hotel_args.location:
        filters["locations"] = hotel_args.location

    # Получаем отели с базовой фильтрацией
    hotels = await HotelsService.get_all(**filters)

    # Дополнительная фильтрация по SPA
    if hotel_args.has_spa is not None:
        if hotel_args.has_spa:
            hotels = [hotel for hotel in hotels
                      if 'SPA' in hotel.services]
        else:
            hotels = [hotel for hotel in hotels
                      if 'SPA' not in hotel.services]
    return hotels
