import logging
from typing import Dict, Any, List
from ..services.weather_service import weather_service

logger = logging.getLogger(__name__)

class WeatherAgent:
    """Monitors live forecast and provides weather risk advisories for the itinerary."""
    def run(self, cities_detail: List[Dict[str, Any]], total_days: int) -> Dict[str, Any]:
        day_forecasts = []
        day_counter = 1

        for city_info in cities_detail:
            city_name = city_info["city"]
            lat = city_info["latitude"]
            lon = city_info["longitude"]
            days_in_city = city_info["days"]

            raw_forecast = weather_service.get_forecast(lat, lon, days=days_in_city)
            for f in raw_forecast:
                if day_counter > total_days:
                    break
                f_day = dict(f)
                f_day["city"] = city_name
                f_day["day_number"] = day_counter
                day_forecasts.append(f_day)
                day_counter += 1

        # Summary flags
        rainy_days = [d["day_number"] for d in day_forecasts if d.get("is_rainy")]
        has_rain_warning = len(rainy_days) > 0

        advisories = []
        if has_rain_warning:
            advisories.append(
                f"Rain showers predicted on Day(s) {', '.join(map(str, rainy_days))}. "
                "Indoor cultural attractions, museums, and covered markets are automatically prioritized."
            )
        else:
            advisories.append("Favorable outdoor sightseeing weather expected across the itinerary.")

        return {
            "forecasts_by_day": day_forecasts,
            "rainy_days": rainy_days,
            "advisories": advisories
        }

weather_agent = WeatherAgent()
