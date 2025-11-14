from configs.logger_config import setup_logger
from clients.currency import convert_krw_to_eur
from schemas.car import CarDataResponse
from selenium import webdriver
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

class CarScraper:
    def __init__(self):
        self.logger = setup_logger("scraper_service")
        self.translator = GoogleTranslator(source='ko', target='en')

    def translate(self, text):
        return self.translator.translate(text) if text else ""

    def calculate_price(self, price_str):
        try:
            price = int(price_str.replace(",", "")) if price_str else 0
        except Exception:
            price = 0
        price_won = (price + 44) * 10000
        return price_won

    def scrape(self, url):
        self.logger.info(f"Starting scrape for URL: {url}")
        driver = webdriver.Chrome()
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        car_name = car_type = car_generation = year = mileage = fuel_type = vehicle_number = price_amount = ""
        main_area = soup.find("div", class_="ResponsiveLayout_content_area__yyYYv")
        if main_area:
            title_tag = main_area.find("h3", class_="DetailSummary_tit_car__0OEVh")
            if title_tag:
                title_spans = title_tag.find_all("span")
                car_name = title_spans[0].get_text(strip=True) if len(title_spans) > 0 else ""
                car_type = title_spans[1].get_text(strip=True) if len(title_spans) > 1 else ""
                car_generation = title_spans[2].get_text(strip=True) if len(title_spans) > 2 else ""

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
            price_eur, currency_error = convert_krw_to_eur(price_won)
            price_amount = price_eur + 1800 if price_eur is not None else None

        image_urls = []
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            data_src = img_tag.get("data-src")
            for url in [src, data_src]:
                if url and url.startswith("https://ci.encar.com/carpicture") and url not in image_urls:
                    image_urls.append(url)

        driver.quit()
        self.logger.info(f"Scraping complete for URL: {url}")

        return CarDataResponse(
            Car_Name=self.translate(car_name),
            Type=self.translate(car_type),
            Generation=self.translate(car_generation),
            Year=self.translate(year),
            Mileage=mileage,
            Fuel_Type=self.translate(fuel_type),
            Vehicle_Number=self.translate(vehicle_number),
            Price=price_amount,
            Images=image_urls,
            CurrencyError=currency_error
        )
