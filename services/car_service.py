from models.car import Car
from services.scraper_service import CarScraper
from services.car_images_service import CarImagesService
import logging

logger = logging.getLogger("autoblur.car_service")


class CarService:
    @staticmethod
    def scrape_car_data(url: str) -> dict:
        scraper = CarScraper()
        car_data = scraper.scrape(url)
        return car_data.model_dump()

    @staticmethod
    def save_car(car_data: dict, db) -> Car:
        car = Car(
            external_id=car_data["Car_External_ID"],
            name=car_data["Car_Name"],
            type=car_data["Type"],
            generation=car_data["Generation"],
            year=car_data["Year"],
            mileage=car_data["Mileage"],
            fuel_type=car_data["Fuel_Type"],
            vehicle_number=car_data["Vehicle_Number"],
            price=car_data["Price"],
        )
        db.add(car)
        db.commit()
        db.refresh(car)
        logger.info(f"Saved car to DB: {car.vehicle_number}")
        return car

    @staticmethod
    def process_car_workflow(url: str, db) -> dict:
        car = CarService.get_car_by_external_id(
            CarScraper.extract_external_id_from_url(url), db
        )
        if car:
            return {"car_id": car.id, "car": {}, "image_ids": []}

        car_data = CarService.scrape_car_data(url)
        image_urls = car_data.get("Images", [])
        car_data.pop("Images", None)  # Remove images from car_data
        car = CarService.save_car(car_data, db)
        image_ids = CarImagesService.save_images(image_urls, db, car.id)
        return {"car_id": car.id, "car": car_data, "image_ids": image_ids}

    @staticmethod
    def get_car_by_external_id(external_id: str, db) -> Car:
        car = db.query(Car).filter(Car.external_id == external_id).first()
        if not car:
            logger.warning(f"Car with external_id {external_id} not found.")
        return car
