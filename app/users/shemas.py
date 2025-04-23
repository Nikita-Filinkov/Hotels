from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class UserShortResponse(BaseModel):
    id: int
    email: str

