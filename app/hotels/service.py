from app.hotels.models import Hotels
from app.service.base import BaseService


class HotelsService(BaseService):
    model = Hotels
