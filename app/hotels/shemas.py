from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, ConfigDict


class SHotels(BaseModel):
    id: int
    name: str
    locations: str
    services: list[str]
    rooms_quantity: int
    image_id: int
    free_rooms: int

    model_config = ConfigDict(from_attributes=True)


class SOneHotels(BaseModel):
    id: int
    name: str
    locations: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


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
