from selenium import webdriver
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from forex_python.converter import CurrencyRates
import asyncio


def scrape_car_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    translator = GoogleTranslator(source='ko', target='en')
    c = CurrencyRates()

    def translate(text):
        return translator.translate(text) if text else ""


    main_area = soup.find("div", class_="ResponsiveLayout_content_area__yyYYv")
    car_name = car_type = car_generation = year = mileage = fuel_type = vehicle_number = price_amount = ""
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
        # Try to find price in the main area
        price_tag = soup.find("div", class_="DetailLeadBottomPc_price_wrap__XlHcb")
        price = ""
        if price_tag:
            price_tag = soup.find("span", class_="DetailLeadCase_point__vdG4b")
            if price_tag:
                price = price_tag.get_text(strip=True)
            else:
                price = 69
        price_won = (int(price.replace(",", "")) + 44) * 10000
        print(f"price_won: {price_won}")
        price_eur = c.convert('KRW', 'EUR', price_won)
        price_eur = round(price_eur, -2)
        print(f"price_eur: {price_eur}")
        price_amount = price_eur + 1800
        print(f"price_amount: {price_amount}")

    # Improved image extraction: collect all src and data-src URLs, avoid duplicates
    image_urls = []
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src")
        data_src = img_tag.get("data-src")
        for url in [src, data_src]:
            if url and url.startswith("https://ci.encar.com/carpicture") and url not in image_urls:
                image_urls.append(url)

    driver.quit()

    return {
        "Car Name": translate(car_name),
        "Type": translate(car_type),
        "Generation": translate(car_generation),
        "Year": translate(year),
        "Mileage": mileage,
        "Fuel Type": translate(fuel_type),
        "Vehicle Number": translate(vehicle_number),
        "Price": price_amount,
        "Images": image_urls
    }
