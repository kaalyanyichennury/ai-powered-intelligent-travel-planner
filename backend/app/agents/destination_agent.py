import logging
from typing import Dict, Any, List
from ..services.places_service import places_service

logger = logging.getLogger(__name__)

# Multi-city splits for countries/destinations
MULTI_CITY_MAP = {
    "italy": [
        {"city": "Rome", "days_share": 0.43, "min_days": 2},
        {"city": "Florence", "days_share": 0.29, "min_days": 2},
        {"city": "Venice", "days_share": 0.28, "min_days": 1},
    ],
    "japan": [
        {"city": "Tokyo", "days_share": 0.45, "min_days": 3},
        {"city": "Kyoto", "days_share": 0.35, "min_days": 2},
        {"city": "Osaka", "days_share": 0.20, "min_days": 1},
    ],
    "spain": [
        {"city": "Barcelona", "days_share": 0.55, "min_days": 3},
        {"city": "Madrid", "days_share": 0.45, "min_days": 2},
    ],
    "france": [
        {"city": "Paris", "days_share": 1.0, "min_days": 3},
    ],
    "united states": [
        {"city": "New York", "days_share": 1.0, "min_days": 3},
    ],
    "united arab emirates": [
        {"city": "Dubai", "days_share": 1.0, "min_days": 3},
    ],
    "indonesia": [
        {"city": "Bali", "days_share": 1.0, "min_days": 3},
    ]
}

class DestinationAgent:
    """Resolves destination cities, multi-city allocations, and geographic centers."""
    def run(self, destination: str, duration_days: int) -> Dict[str, Any]:
        dest_clean = destination.strip()
        dest_lower = dest_clean.lower()

        # Check if destination corresponds to a multi-city country route
        cities_plan = []
        if dest_lower in MULTI_CITY_MAP and duration_days >= 5:
            city_splits = MULTI_CITY_MAP[dest_lower]
            remaining_days = duration_days
            for i, split in enumerate(city_splits):
                if i == len(city_splits) - 1:
                    days_assigned = max(1, remaining_days)
                else:
                    days_assigned = max(1, int(round(duration_days * split["days_share"])))
                    remaining_days -= days_assigned

                geo = places_service.geocode_destination(split["city"])
                cities_plan.append({
                    "city": split["city"],
                    "days": days_assigned,
                    "latitude": geo["latitude"],
                    "longitude": geo["longitude"],
                    "country": geo.get("country", dest_clean)
                })
        else:
            # Single primary destination city
            geo = places_service.geocode_destination(dest_clean)
            cities_plan.append({
                "city": geo["city"],
                "days": duration_days,
                "latitude": geo["latitude"],
                "longitude": geo["longitude"],
                "country": geo.get("country", dest_clean)
            })

        return {
            "primary_destination": dest_clean,
            "country": cities_plan[0].get("country", dest_clean),
            "cities": [c["city"] for c in cities_plan],
            "cities_detail": cities_plan
        }

destination_agent = DestinationAgent()
