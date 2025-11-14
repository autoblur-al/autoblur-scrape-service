from sqlalchemy import Column, Integer, String, Float
from models.base import Base

class Car(Base):
    __tablename__ = "cars"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    generation = Column(String)
    year = Column(String)
    mileage = Column(String)
    fuel_type = Column(String)
    vehicle_number = Column(String)
    price = Column(Float)
