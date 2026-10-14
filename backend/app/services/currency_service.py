import logging
import requests
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "INR": "₹",
    "GBP": "£",
    "JPY": "¥",
    "CAD": "CA$",
    "AUD": "A$",
    "AED": "AED ",
    "SGD": "S$",
    "CHF": "CHF ",
    "THB": "฿",
}

# Reliable fallback base USD exchange rates in case API is offline
FALLBACK_RATES_TO_USD = {
    "USD": 1.0,
    "EUR": 0.92,
    "INR": 83.5,
    "GBP": 0.79,
    "JPY": 154.0,
    "CAD": 1.36,
    "AUD": 1.52,
    "AED": 3.67,
    "SGD": 1.35,
    "CHF": 0.90,
    "THB": 36.5,
}

class CurrencyService:
    _cached_rates: Dict[str, float] = FALLBACK_RATES_TO_USD.copy()
    _rates_loaded: bool = False

    @classmethod
    def get_symbol(cls, currency_code: str) -> str:
        return CURRENCY_SYMBOLS.get(currency_code.upper(), f"{currency_code} ")

    @classmethod
    def refresh_rates(cls):
        try:
            url = "https://open.er-api.com/v6/latest/USD"
            resp = requests.get(url, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                if "rates" in data:
                    cls._cached_rates = data["rates"]
                    cls._rates_loaded = True
                    logger.info("Successfully refreshed live global currency rates from open.er-api.com")
        except Exception as e:
            logger.warning(f"Could not reach external currency API, using fallback exchange rates: {e}")

    @classmethod
    def convert(cls, amount: float, from_curr: str, to_curr: str) -> float:
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        if from_curr == to_curr:
            return round(amount, 2)

        rates = cls._cached_rates if cls._rates_loaded else FALLBACK_RATES_TO_USD
        from_rate = rates.get(from_curr, 1.0)
        to_rate = rates.get(to_curr, 1.0)

        # Convert to USD first, then to target currency
        amount_in_usd = amount / from_rate if from_rate else amount
        result = amount_in_usd * to_rate
        return round(result, 2)

    @classmethod
    def format_amount(cls, amount: float, currency_code: str) -> str:
        symbol = cls.get_symbol(currency_code)
        if currency_code.upper() in ["INR", "JPY"]:
            return f"{symbol}{amount:,.0f}"
        return f"{symbol}{amount:,.2f}"

currency_service = CurrencyService()
