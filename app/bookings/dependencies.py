from datetime import datetime

from fastapi import HTTPException, Request, Depends, status
import jwt
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import PyJWTError, InvalidTokenError
from app.config import settings
from app.exceptions import (TokenExpiredException, TokenAbsentException, UserIdNotInJWTException,
                            UserNotFoundException, TokenInvalidFormatException)
from app.users.service import UsersService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/loging")


def get_jwt_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if token:
        return token
    raise TokenAbsentException


async def get_current_user(
        token: str = Depends(get_jwt_token)
):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    # try:
    #     payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    # except InvalidTokenError:
    #     raise TokenInvalidFormatException
    expire: str = payload.get('exp')
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if user_id is None:
        raise UserIdNotInJWTException
    user = await UsersService.find_by_id(int(user_id))
    if user is None:
        raise UserNotFoundException
    return user

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