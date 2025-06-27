from datetime import datetime, timezone

import jwt
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.exceptions import (
    TokenAbsentException,
    TokenExpiredException,
    TokenInvalidFormatException,
    UserIdNotInJWTException,
    UserNotFoundException,
)
from app.users.service import UsersService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_jwt_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if token:
        return token
    raise TokenAbsentException


async def get_current_user(
        token: str = Depends(get_jwt_token)
):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if user_id is None:
        raise UserIdNotInJWTException
    user = await UsersService.find_by_id(int(user_id))
    if user is None:
        raise UserNotFoundException
    return user

