from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.bookings.dependencies import get_current_user
from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import auth_user, create_access_token, get_password_hash
from app.users.models import Users
from app.users.service import UsersService
from app.users.shemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post('/register')
async def register_user(register_date: SUserAuth):
    existing_user = await UsersService.find_one_or_none(email=register_date.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(register_date.password)
    await UsersService.add(email=register_date.email, hashed_password=hashed_password)


@router.post('/login')
async def loging_user(response: Response, user_date: SUserAuth):
    user = await auth_user(email=user_date.email, password=user_date.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post('logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
