from db.database import SessionLocal
from models.car import Car
from services.scraper_service import CarScraper
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

    @staticmethod
    def save_images(image_urls: list[str], db, car_id: int) -> list[int]:
            logger.info(f"image URLs: {image_urls}")
            scraper = CarScraper()
            image_ids = []
            used_orders = set()
            for idx, url in enumerate(image_urls):
                # Extract order number from URL
                order_num = None
                try:
                    filename = url.split("/")[-1]
                    order_part = filename.split("_")[-1].split(".")[0]
                    order_num = int(order_part)
                    logger.info(f"Extracted order number {order_num} from URL: {url}")
                except Exception:
                    logger.warning(f"Failed to extract order number from URL: {url}")
                # Ensure order_num is unique and valid
                if order_num is None or order_num in used_orders:
                    order_num = idx + 1  # fallback to index, ensures uniqueness
                used_orders.add(order_num)
                path = scraper.download_and_save_image(url, car_id, order_num)
                if path:
                    from models.car_image import CarImage
                    car_image = CarImage(path=path, car_id=car_id, order=order_num)
                    db.add(car_image)
                    db.commit()
                    db.refresh(car_image)
                    image_ids.append(car_image.id)
            return image_ids

    @staticmethod
    def process_car_workflow(url: str, db) -> dict:
        car_data = CarService.scrape_car_data(url)
        image_urls = car_data.get("Images", [])
        car_data.pop("Images", None)  # Remove images from car_data
        car = CarService.save_car(car_data, db)
        image_ids = CarService.save_images(image_urls, db, car.id)
        return {
            "car_id": car.id,
            "car": car_data,
            "image_ids": image_ids
        }

    @staticmethod
    def get_image_bytes_by_id(image_id: int, db) -> bytes:
        from models.car_image import CarImage
        image = db.query(CarImage).filter(CarImage.id == image_id).first()
        if not image:
            logger.warning(f"Image with id {image_id} not found.")
            return None
        try:
            with open(image.path, "rb") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to read image file {image.path}: {e}")
            return None
