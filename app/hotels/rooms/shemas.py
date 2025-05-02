from pydantic import BaseModel


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int
    free_rooms: int

    class Config:
        from_attributes = True  # Для автоматического преобразования ORM-модели