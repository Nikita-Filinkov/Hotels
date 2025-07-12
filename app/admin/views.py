from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import User


class UsersAdmin(ModelView, model=User):
    column_list = [User.id, User.email] + [User.booking]
    can_delete = False
    column_details_exclude_list = [User.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-regular fa-circle-user"
    category = "Управление пользователями"
    category_icon = "fa-solid fa-user"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user] + [Bookings.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-calendar-check"
    category = "Управление бронированием"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.room]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-bed"
    category = "Управление бронированием"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-key"
    category = "Управление бронированием"

