from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = 'password'


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


pass_hash1 = get_password_hash(password)
pass_hash2 = get_password_hash(password)
print(pass_hash1)
print(pass_hash2)

is_correct1 = verify_password(password, pass_hash1)
is_correct2 = verify_password(password, pass_hash2)

print(is_correct1)
print(is_correct2)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        ALGORITHM
    )
    return encoded_jwt


data = {'user': 'Nikita'}
print(create_access_token(data))


def create_admin_access_token(data: dict) -> str:
    # Добавляем специальный claim для админки
    data.update({"is_admin": True})
    return create_access_token(data)

