from datetime import date

from app.hotels.router import router


@router.get('/{hotel_id}')
async def get_empty_rooms(
        hotel_id: int,
        date_from: date,
        date_to: date
):
    pass
