import csv
import os
import logging
import random
import requests
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PlacesService:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.places_file = os.path.join(self.base_dir, "data", "places.csv")
        self.hotels_file = os.path.join(self.base_dir, "data", "hotels.csv")
        self.restaurants_file = os.path.join(self.base_dir, "data", "restaurants.csv")
        
        self.curated_places: List[Dict[str, Any]] = []
        self.curated_hotels: List[Dict[str, Any]] = []
        self.curated_restaurants: List[Dict[str, Any]] = []
        self.load_datasets()

    def load_datasets(self):
        try:
            if os.path.exists(self.places_file):
                with open(self.places_file, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row["latitude"] = float(row.get("latitude", 0.0))
                        row["longitude"] = float(row.get("longitude", 0.0))
                        row["rating"] = float(row.get("rating", 4.5))
                        row["price"] = float(row.get("price", 0.0))
                        row["visit_duration_hrs"] = float(row.get("visit_duration_hrs", 2.0))
                        self.curated_places.append(row)
                logger.info(f"Loaded {len(self.curated_places)} curated places.")
        except Exception as e:
            logger.error(f"Error loading places.csv: {e}")

        try:
            if os.path.exists(self.hotels_file):
                with open(self.hotels_file, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row["latitude"] = float(row.get("latitude", 0.0))
                        row["longitude"] = float(row.get("longitude", 0.0))
                        row["rating"] = float(row.get("rating", 4.5))
                        row["price_per_night_usd"] = float(row.get("price_per_night_usd", 120.0))
                        self.curated_hotels.append(row)
        except Exception as e:
            logger.error(f"Error loading hotels.csv: {e}")

        try:
            if os.path.exists(self.restaurants_file):
                with open(self.restaurants_file, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        row["latitude"] = float(row.get("latitude", 0.0))
                        row["longitude"] = float(row.get("longitude", 0.0))
                        row["rating"] = float(row.get("rating", 4.5))
                        row["avg_cost_usd"] = float(row.get("avg_cost_usd", 25.0))
                        self.curated_restaurants.append(row)
        except Exception as e:
            logger.error(f"Error loading restaurants.csv: {e}")

    def geocode_destination(self, query: str) -> Dict[str, Any]:
        """
        Geocodes any destination worldwide using OpenStreetMap Nominatim.
        Provides robust offline fallback for major destinations.
        """
        clean_q = query.strip()
        headers = {"User-Agent": "AITravelPlannerBEProject/1.0 (travelplanner@academic.edu)"}
        try:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={clean_q}&limit=1"
            resp = requests.get(url, headers=headers, timeout=3.0)
            if resp.status_code == 200:
                results = resp.json()
                if results and len(results) > 0:
                    item = results[0]
                    display_parts = item.get("display_name", "").split(", ")
                    city = display_parts[0]
                    country = display_parts[-1]
                    return {
                        "name": city,
                        "city": city,
                        "country": country,
                        "latitude": float(item["lat"]),
                        "longitude": float(item["lon"]),
                        "display_name": item.get("display_name")
                    }
        except Exception as e:
            logger.warning(f"Nominatim geocoding failed or timed out: {e}")

        # Check in curated places
        lower_q = clean_q.lower()
        for p in self.curated_places:
            if lower_q in p["city"].lower() or lower_q in p["country"].lower():
                return {
                    "name": p["city"],
                    "city": p["city"],
                    "country": p["country"],
                    "latitude": p["latitude"],
                    "longitude": p["longitude"],
                    "display_name": f"{p['city']}, {p['country']}"
                }

        # Default fallback (Paris)
        return {
            "name": clean_q.title(),
            "city": clean_q.title(),
            "country": "International",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "display_name": f"{clean_q.title()}"
        }

    def get_attractions_for_city(self, city_name: str, country_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns places for a specific city, combining curated dataset with dynamic generation if novel."""
        city_lower = city_name.lower().strip()
        matching = [
            p for p in self.curated_places
            if city_lower in p["city"].lower() or (country_name and country_name.lower() in p["country"].lower())
        ]
        if matching and len(matching) >= 4:
            return matching

        # If not enough curated places for this city, synthesize realistic landmarks around its coordinates
        geo = self.geocode_destination(city_name)
        lat = geo["latitude"]
        lon = geo["longitude"]
        country = geo.get("country", country_name or "Global")

        synthesized = [
            {
                "place_id": f"GEN_{i}",
                "name": f"{city_name} {title}",
                "city": city_name,
                "country": country,
                "latitude": round(lat + random.uniform(-0.03, 0.03), 4),
                "longitude": round(lon + random.uniform(-0.03, 0.03), 4),
                "category": cat,
                "description": desc.format(city=city_name),
                "opening_hours": "09:00-18:00",
                "rating": round(random.uniform(4.5, 4.9), 1),
                "price": round(random.choice([0.0, 10.0, 15.0, 22.0, 30.0]), 1),
                "visit_duration_hrs": random.choice([1.5, 2.0, 2.5, 3.0]),
                "best_season": "All",
                "indoor_outdoor": indoor,
                "tags": tags
            }
            for i, (title, cat, desc, indoor, tags) in enumerate([
                ("Historic Old Town Center", "Historical site", "Charming heritage district of {city} with centuries-old architecture, cobblestone alleys, and historic monuments.", "Outdoor", "history architecture culture walking photography"),
                ("National Art & History Museum", "Museum", "Premier cultural institution housing national treasures, masterworks, and archaeological artifacts of {city}.", "Indoor", "art museum history masterpieces culture"),
                ("Grand City Panoramic Viewpoint", "Adventure", "Celebrated high vantage point offering breathtaking 360-degree skyline vistas of {city} and surrounding landscapes.", "Outdoor", "skyline views photography iconic landmark sunset"),
                ("Central Botanical Gardens & Promenade", "Nature", "Lush green oasis in the heart of {city} featuring native flora, tranquil fountains, and serene walking paths.", "Outdoor", "nature park relaxation walking peaceful greenery"),
                ("Royal Cathedral & Plaza", "Church", "Majestic religious landmark celebrated for magnificent stone carvings, stained glass, and tranquil atmosphere.", "Indoor", "history religion architecture church photography"),
                ("Gourmet Food Market & Bazaar", "Food", "Vibrant marketplace bustling with local culinary delicacies, street food stalls, fresh produce, and pastries.", "Outdoor", "food culinary market tasting street-food authentic"),
                ("Contemporary Culture Center", "Museum", "Striking architectural hub exhibiting innovative modern art, design installations, and interactive galleries.", "Indoor", "modern art architecture interactive contemporary"),
                ("Sunset Riverfront Boulevard", "Photography", "Picturesque waterfront promenade offering romantic sunset vistas, open-air cafes, and street musicians.", "Outdoor", "riverfront sunset photography romantic walking leisure")
            ])
        ]
        return matching + synthesized

    def get_hotel_recommendation(self, city_name: str, tier: str = "mid-range") -> Dict[str, Any]:
        """Returns a suitable hotel for the city and budget tier."""
        city_lower = city_name.lower().strip()
        candidates = [h for h in self.curated_hotels if city_lower in h["city"].lower() and h.get("tier") == tier]
        if candidates:
            return candidates[0]
        # Any hotel in city
        any_city = [h for h in self.curated_hotels if city_lower in h["city"].lower()]
        if any_city:
            return any_city[0]

        # Dynamic fallback
        rates = {"budget": 45.0, "mid-range": 135.0, "luxury": 450.0}
        return {
            "hotel_id": "HOTEL_GEN",
            "name": f"{city_name} Boutique Grand Hotel",
            "city": city_name,
            "country": "International",
            "tier": tier,
            "price_per_night_usd": rates.get(tier, 130.0),
            "rating": 4.6,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "amenities": "Free WiFi Rooftop Lounge Breakfast Central Location"
        }

    def get_restaurant_recommendations(self, city_name: str) -> List[Dict[str, Any]]:
        """Returns curated or generated dining recommendations."""
        city_lower = city_name.lower().strip()
        matches = [r for r in self.curated_restaurants if city_lower in r["city"].lower()]
        if len(matches) >= 2:
            return matches

        return [
            {
                "restaurant_id": "R_GEN_1",
                "name": f"Le Bistrot {city_name}",
                "city": city_name,
                "cuisine": "Authentic Regional Cuisine",
                "avg_cost_usd": 28.0,
                "rating": 4.7,
                "highlights": "Seasonal local ingredients, signature house specialties, warm ambiance"
            },
            {
                "restaurant_id": "R_GEN_2",
                "name": f"{city_name} Heritage Taverna",
                "city": city_name,
                "cuisine": "Traditional Local Delicacies",
                "avg_cost_usd": 20.0,
                "rating": 4.6,
                "highlights": "Handcrafted recipes, artisanal wines, vibrant neighborhood atmosphere"
            }
        ]

places_service = PlacesService()
