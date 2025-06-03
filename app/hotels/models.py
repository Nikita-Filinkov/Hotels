from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = 'hotels'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    locations = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer)
    image_id = Column(Integer)

    room = relationship("Rooms", back_populates="hotel")

    def __str__(self):
        return f"Отель: {self.name}"




