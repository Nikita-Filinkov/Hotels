from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)