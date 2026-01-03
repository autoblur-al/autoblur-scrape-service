from bs4 import BeautifulSoup
from services.scraper_service import CarScraper


# Helper to simulate scraping from HTML file instead of Selenium
class TestCarScraper(CarScraper):
    def scrape_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        # Copy-paste the parsing logic from CarScraper.scrape, but use soup directly
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
            price_eur = 1000  # Mocked currency conversion
            price_amount = price_eur + 1800 if price_eur is not None else None

        image_urls = []
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

        return {
            "Car Name": self.translate(car_name),
            "Type": self.translate(car_type),
            "Generation": self.translate(car_generation),
            "Year": self.translate(year),
            "Mileage": mileage,
            "Fuel Type": self.translate(fuel_type),
            "Vehicle Number": vehicle_number,  # Do not translate
            "Price": price_amount,
            "Images": image_urls,
        }
