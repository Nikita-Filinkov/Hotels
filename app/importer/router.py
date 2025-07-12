from fastapi import APIRouter, UploadFile, HTTPException, status
import json

from sqlalchemy import insert

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import User

router = APIRouter(
    prefix='/import',
    tags=['Загрузка данных']
)


@router.post('/{table_name}')
async def add_hotel(table_name: str, file: UploadFile):

    if table_name == 'hotels':
        tabel = Hotels
    elif table_name == 'rooms':
        tabel = Rooms
    elif table_name == 'users':
        tabel = User
    elif table_name == 'bookings':
        tabel = Bookings
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Не корректные данные')

    try:
        contents = await file.read()
        data = json.loads(contents)
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Не корректные данные')
    
    async with async_session_maker() as session:
        add_hotels = insert(tabel).values(data)
        await session.execute(add_hotels)
        await session.commit()

    return {"status": "success", "table": table_name, "filename": file.filename}
