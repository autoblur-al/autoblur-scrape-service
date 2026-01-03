import requests
from configs.logger_config import setup_logger

logger = setup_logger("currency_api")


def convert_krw_to_eur(amount):
    """
    Convert KRW to EUR using exchangerate-api.com
    Returns (converted_amount, error_flag)
    """
    try:
        response = requests.get("https://open.er-api.com/v6/latest/KRW")
        data = response.json()
        eur_rate = data["rates"].get("EUR")
        if eur_rate:
            converted = round(amount * eur_rate, -2)
            return converted
        else:
            logger.error("EUR rate not found in API response.")
            return None
    except Exception as e:
        logger.error(f"Currency conversion failed: {e}")
        return None
