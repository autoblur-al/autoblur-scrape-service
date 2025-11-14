from db.database import SessionLocal
from models.car import Car
import logging

logger = logging.getLogger("autoblur.car_service")

class CarService:
    @staticmethod
    def save_car(car_data: dict, db) -> Car:
        """
        Save car data to the database, skipping images.
        car_data keys: Car_Name, Type, Generation, Year, Mileage, Fuel_Type, Vehicle_Number, Price
        """
        car = Car(
            name=car_data["Car_Name"],
            type=car_data["Type"],
            generation=car_data["Generation"],
            year=car_data["Year"],
            mileage=car_data["Mileage"],
            fuel_type=car_data["Fuel_Type"],
            vehicle_number=car_data["Vehicle_Number"],
            price=car_data["Price"]
        )
        db.add(car)
        db.commit()
        db.refresh(car)
        logger.info(f"Saved car to DB: {car.vehicle_number}")
        return car
