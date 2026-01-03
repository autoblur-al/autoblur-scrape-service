from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class CarImage(Base):
    __tablename__ = "car_images"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=True)
    url = Column(String, nullable=False)
    order = Column(Integer, nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"))
    car = relationship("Car", back_populates="images")
