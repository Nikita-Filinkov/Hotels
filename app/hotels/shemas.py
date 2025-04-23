from pydantic import BaseModel
from typing import Optional
from datetime import date
from fastapi import Query


class SHotel(BaseModel):
    id: int
    name: str
    locations: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True  # Для автоматического преобразования ORM-модели


class HotelsArgs:
    def __init__(self,
                 location: str,
                 date_from: date,
                 date_to: date,
                 has_spa: Optional[bool] = None,
                 stars: Optional[int] = Query(None, ge=1, le=5),
                 ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars
