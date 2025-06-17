from __future__ import annotations

import asyncio
from datetime import date

from fastapi import APIRouter, Depends, Query

from fastapi_cache.decorator import cache

from app.hotels.shemas import HotelsArgs, SOneHotels, SHotels
from app.hotels.service import HotelsService

from pydantic import parse_obj_as



# @router.post('/loging')
# async def loging_user(response: Response, user_date: SUserAuth):
#     user = await auth_user(email=user_date.email, password=user_date.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#
#     access_token = create_access_token({'sub': user.id})
#     response.set_cookie("booking_access_token", access_token, httponly=True)
#     return access_token

# @router.get('/{locations}', response_model=list[SHotels])
# @cache(expire=60)
# async def hotels_on_location(
#         locations: str,
#         date_from: date = Query(description=f"Например: 2023-05-15"),
#         date_to: date = Query(description=f"Например: 2023-06-30")
# ):
#     await asyncio.sleep(3)
#     free_hotels = await HotelsService.get_hotels_on_location(
#         locations=locations,
#         date_from=date_from,
#         date_to=date_to
#     )
#     # Нужно для валидации, так как redis принимает только простые данные типа list, dict, str и т.д
#     print(type(free_hotels[0]))
#     free_hotels = parse_obj_as(list[SHotels], free_hotels)
#     print(type(free_hotels[0]))
#
#     return free_hotels

# Для открытия Flower
# Должен быть запущен Redis
# Должен быть запущен worker
# http://localhost:5555/

# def get_current_user(token: str = Depends(oauth2_scheme)):
#
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},)
#
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         user = UsersService.find_by_id(user_id)
#     except InvalidTokenError:
#         raise credentials_exception
#
#     return user

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("test"))  # Должно работать без ошибок