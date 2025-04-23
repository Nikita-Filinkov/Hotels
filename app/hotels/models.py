from sqlalchemy import Column, Integer, String, JSON, ForeignKey

from app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    locations = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer)
    image_id = Column(Integer)


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    price = Column(Integer)
    quantity = Column(Integer)
    services = Column(JSON)
    image_id = Column(Integer)

