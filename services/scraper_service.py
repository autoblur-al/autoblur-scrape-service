from configs.logger_config import setup_logger
from clients.currency import convert_krw_to_eur
from schemas.car import CarDataResponse
from models.car_image import CarImage
from db.deps import get_db
from selenium import webdriver
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

logger = setup_logger("scraper_service")


class CarScraper:
    def __init__(self):
        self.logger = setup_logger("scraper_service")
        self.translator = GoogleTranslator(source="ko", target="en")

    def translate(self, text):
        return self.translator.translate(text) if text else ""

    def calculate_price(self, price_str):
        try:
            price = int(price_str.replace(",", "")) if price_str else 0
        except Exception:
            price = 0
        price_won = (price + 44) * 10000
        return price_won

    def scrape(self, url, db=None, car_id=None):
        self.logger.info(f"Starting scrape for URL: {url}")
        try:
            car_external_id = self.extract_external_id_from_url(url)
            self.logger.info("Launching Chrome WebDriver...")
            driver = webdriver.Chrome()
            self.logger.info("Chrome WebDriver launched successfully.")
        except Exception as e:
            self.logger.error(f"Failed to launch Chrome WebDriver: {e}")
            raise
        try:
            self.logger.info(f"Navigating to {url}")
            driver.get(url)
            self.logger.info("Navigation complete. Fetching page source...")
            page_source = driver.page_source
            self.logger.info(f"Page source length: {len(page_source)}")
            soup = BeautifulSoup(page_source, "html.parser")
        except Exception as e:
            self.logger.error(f"Error during navigation or page source fetch: {e}")
            driver.quit()
            raise

        car_name = car_type = car_generation = year = mileage = fuel_type = (
            vehicle_number
        ) = price_amount = ""
        main_area = soup.find("div", class_="ResponsiveLayout_content_area__yyYYv")
        if main_area:
            title_tag = main_area.find("h3", class_="DetailSummary_tit_car__0OEVh")
            if title_tag:
                title_spans = title_tag.find_all("span")
                car_name = (
                    title_spans[0].get_text(strip=True) if len(title_spans) > 0 else ""
                )
                car_type = (
                    title_spans[1].get_text(strip=True) if len(title_spans) > 1 else ""
                )
                car_generation = (
                    title_spans[2].get_text(strip=True) if len(title_spans) > 2 else ""
                )

            summary = main_area.find("dl", class_="DetailSummary_define_summary__NOYid")
            if summary:
                for dt, dd in zip(summary.find_all("dt"), summary.find_all("dd")):
                    key = dt.get_text(strip=True)
                    value = dd.get_text(strip=True)
                    if "연식" in key:
                        year = value
                    elif "주행거리" in key:
                        mileage = value
                    elif "연료" in key:
                        fuel_type = value
                    elif "차량번호" in key:
                        vehicle_number = value

            price_tag = soup.find("div", class_="DetailLeadBottomPc_price_wrap__XlHcb")
            price_str = ""
            if price_tag:
                price_tag = soup.find("span", class_="DetailLeadCase_point__vdG4b")
                if price_tag:
                    price_str = price_tag.get_text(strip=True)
                else:
                    price_str = "69"
            price_won = self.calculate_price(price_str)
            price_eur = convert_krw_to_eur(price_won)
            self.logger.info(f"KRW to EUR conversion result: {price_eur}")
            try:
                price_amount = float(price_eur) + 1800
            except (TypeError, ValueError):
                self.logger.warning(f"Price conversion failed, got value: {price_eur}")
                price_amount = None

        image_urls = []
        image_paths = []
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            data_src = img_tag.get("data-src")
            for url in [src, data_src]:
                if (
                    url
                    and url.startswith("https://ci.encar.com/carpicture")
                    and url not in image_urls
                ):
                    image_urls.append(url)
                    # Extract order number from URL
                    order_num = None
                    try:
                        # Example: .../40606713_024.jpg?
                        filename = url.split("/")[-1]
                        order_part = filename.split("_")[-1].split(".")[0]  # '024'
                        order_num = int(order_part)
                    except Exception:
                        order_num = 0
                    if db and car_id:
                        path = self.download_and_save_image(url, car_id, order_num)
                        if path:
                            image_paths.append(path)
                            car_image = CarImage(
                                path=path, car_id=car_id, order=order_num
                            )
                            db.add(car_image)
        if db:
            db.commit()

        self.logger.info("Quitting Chrome WebDriver...")
        driver.quit()
        self.logger.info(f"Scraping complete for URL: {url}")

        return CarDataResponse(
            Car_External_ID=car_external_id,
            Car_Name=self.translate(car_name),
            Type=self.translate(car_type),
            Generation=self.translate(car_generation),
            Year=self.translate(year),
            Mileage=mileage,
            Fuel_Type=self.translate(fuel_type),
            Vehicle_Number=self.translate(vehicle_number),
            Price=price_amount,
            Images=image_paths if image_paths else image_urls,
        )

    @staticmethod
    def extract_external_id_from_url(url: str) -> str:
        try:
            parts = url.split("/detail/")
            if len(parts) > 1:
                external_id = parts[1].split("?")[0]
                return external_id
            return None
        except Exception as e:
            logger.error(f"Failed to extract external ID from URL {url}: {e}")
            return None
