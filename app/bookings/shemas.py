from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class SBookings(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: int
    name: str
    description: str | None = None
    services: list[str]
