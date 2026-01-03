import os
import requests
from db.database import SessionLocal
from models.car import Car
from services.scraper_service import CarScraper
import logging

logger = logging.getLogger("autoblur.car_images_service")


class CarImagesService:
    @staticmethod
    def _extract_order_from_url(url: str) -> int | None:
        """Extract order number from image URL filename.

        Expects format: .../filename_123.ext where 123 is the order number.
        Returns None if extraction fails.
        """
        try:
            filename = url.split("/")[-1]
            order_part = filename.split("_")[-1].split(".")[0]
            order_num = int(order_part)
            logger.info(f"Extracted order number {order_num} from URL: {url}")
            return order_num
        except Exception:
            logger.warning(f"Failed to extract order number from URL: {url}")
            return None

    @staticmethod
    def _get_unique_order_number(
        order_num: int | None, idx: int, used_orders: set
    ) -> int:
        """Ensure order number is unique and valid, using index as fallback."""
        if order_num is None or order_num in used_orders:
            order_num = idx + 1
        return order_num

    @staticmethod
    def _save_single_image(
        url: str, car_id: int, order_num: int, download: bool, db
    ) -> int | None:
        """Download, save, and persist a single car image.

        Returns the image ID if successful, None otherwise.
        """
        path = None
        if download:
            path = CarImagesService.download_and_save_image(url, car_id, order_num)

        from models.car_image import CarImage

        car_image = CarImage(url=url, path=path, car_id=car_id, order=order_num)
        db.add(car_image)
        db.commit()
        db.refresh(car_image)
        return car_image.id

    @staticmethod
    def save_images(
        image_urls: list[str], db, car_id: int, download: bool
    ) -> list[int]:
        """Save multiple car images from URLs.

        Downloads images, extracts order numbers, and persists to database.
        Returns list of created image IDs.
        """
        logger.info(f"image URLs: {image_urls}")
        scraper = CarScraper()
        image_ids = []
        used_orders = set()

        for idx, url in enumerate(image_urls):
            order_num = CarImagesService._extract_order_from_url(url)
            order_num = CarImagesService._get_unique_order_number(
                order_num, idx, used_orders
            )
            used_orders.add(order_num)

            image_id = CarImagesService._save_single_image(
                url, car_id, order_num, download, db
            )
            if image_id:
                image_ids.append(image_id)

        return image_ids

    @staticmethod
    def get_image_bytes_by_id(image_id: int, db) -> bytes | None:
        """Retrieve image file bytes by image ID.

        Returns image bytes if found and readable, None otherwise.
        """
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

    @staticmethod
    def get_image_ids_by_car_id(car_id: int, db) -> list[int] | None:
        """Get all image IDs associated with a car.

        Returns list of image IDs if found, None if no images exist.
        """
        from models.car_image import CarImage

        images = db.query(CarImage).filter(CarImage.car_id == car_id).all()
        if not images:
            logger.warning(f"No images found for car_id {car_id}.")
            return None
        return [image.id for image in images]

    def download_and_save_image(
        self, image_url: str, car_id: int, order_num: int, save_dir: str = None
    ) -> str:
        # Use settings for image save directory
        from configs.settings import settings

        if save_dir is None:
            save_dir = settings.car_image_save_dir
        os.makedirs(save_dir, exist_ok=True)
        filename = f"car_{car_id}_img_{order_num}.jpg"
        file_path = os.path.join(save_dir, filename)
        logger.info(f"Downloading image from {image_url} to {file_path}")
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return file_path
        else:
            self.logger.error(f"Failed to download image: {image_url}")
            return None
