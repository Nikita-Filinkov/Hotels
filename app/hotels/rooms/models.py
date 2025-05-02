from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer)
    quantity = Column(Integer)
    services = Column(JSON)
    image_id = Column(Integer)
