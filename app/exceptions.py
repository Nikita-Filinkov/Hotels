from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class TokenInvalidFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIdNotInJWTException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Id не был передан"


class UserNotFoundException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED


class RoomCannotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class BookingsCannotFound(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "У вас ничего не забронировано"


class ProhibitedDeleteException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Бронирование не найдено или не принадлежит пользователю"
