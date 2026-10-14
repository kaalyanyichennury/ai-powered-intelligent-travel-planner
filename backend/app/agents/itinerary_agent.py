import logging
from typing import Dict, Any, List
from ..services.maps_service import maps_service
from ..services.places_service import places_service
from ..services.currency_service import currency_service
from ..schemas.travel_schemas import DayPlan, ActivitySlot

logger = logging.getLogger(__name__)

class ItineraryAgent:
    """Constructs geographically optimized, day-by-day travel schedules."""
    def run(
        self,
        cities_detail: List[Dict[str, Any]],
        attractions: List[Dict[str, Any]],
        weather_data: Dict[str, Any],
        currency: str,
        total_days: int
    ) -> List[DayPlan]:
        day_plans = []
        forecasts = weather_data.get("forecasts_by_day", [])
        
        # Build day-to-city map
        city_schedule = []
        for c in cities_detail:
            for _ in range(c["days"]):
                city_schedule.append(c["city"])

        # Group attractions by city
        places_pool: Dict[str, List[Dict[str, Any]]] = {}
        for p in attractions:
            city_key = p.get("city", "Default")
            if city_key not in places_pool:
                places_pool[city_key] = []
            places_pool[city_key].append(p)

        used_place_ids = set()

        for day_num in range(1, total_days + 1):
            target_city = city_schedule[day_num - 1] if day_num - 1 < len(city_schedule) else cities_detail[0]["city"]
            forecast = forecasts[day_num - 1] if day_num - 1 < len(forecasts) else {}
            is_rainy = forecast.get("is_rainy", False)

            available = places_pool.get(target_city, [])
            unused = [p for p in available if p.get("place_id") not in used_place_ids]
            if len(unused) < 3:
                # If exhausted, replenish
                unused = available

            # Separate indoor and outdoor for weather adaptation
            indoor_picks = [p for p in unused if str(p.get("indoor_outdoor", "")).lower() == "indoor"]
            outdoor_picks = [p for p in unused if str(p.get("indoor_outdoor", "")).lower() == "outdoor"]

            day_places = []
            if is_rainy and indoor_picks:
                # Prioritize indoor museum/cultural sites
                day_places.append(indoor_picks[0])
                used_place_ids.add(indoor_picks[0].get("place_id"))
                if len(indoor_picks) > 1:
                    day_places.append(indoor_picks[1])
                    used_place_ids.add(indoor_picks[1].get("place_id"))
                elif outdoor_picks:
                    day_places.append(outdoor_picks[0])
                    used_place_ids.add(outdoor_picks[0].get("place_id"))
            else:
                # Standard balanced mix
                if outdoor_picks:
                    day_places.append(outdoor_picks[0])
                    used_place_ids.add(outdoor_picks[0].get("place_id"))
                if indoor_picks:
                    day_places.append(indoor_picks[0])
                    used_place_ids.add(indoor_picks[0].get("place_id"))

            # Fill up to 3 attractions
            for p in unused:
                if len(day_places) >= 3:
                    break
                if p.get("place_id") not in used_place_ids:
                    day_places.append(p)
                    used_place_ids.add(p.get("place_id"))

            # Fallback if somehow still empty
            if not day_places and available:
                day_places = available[:3]

            # Optimize geographic route for the day
            optimized_stops = maps_service.optimize_route(day_places)

            # Get dinner restaurant for city
            restaurants = places_service.get_restaurant_recommendations(target_city)
            dinner_venue = restaurants[(day_num - 1) % len(restaurants)]

            # Build activity slots
            m_stop = optimized_stops[0] if len(optimized_stops) > 0 else {}
            a_stop = optimized_stops[1] if len(optimized_stops) > 1 else m_stop
            e_stop = optimized_stops[2] if len(optimized_stops) > 2 else a_stop

            # Calculate transit leg: Morning -> Afternoon
            dist_1 = maps_service.haversine_distance_km(
                m_stop.get("latitude", 0.0), m_stop.get("longitude", 0.0),
                a_stop.get("latitude", 0.0), a_stop.get("longitude", 0.0)
            )
            transit_1 = maps_service.calculate_transit_times(dist_1)

            # Calculate transit leg: Afternoon -> Evening
            dist_2 = maps_service.haversine_distance_km(
                a_stop.get("latitude", 0.0), a_stop.get("longitude", 0.0),
                e_stop.get("latitude", 0.0), e_stop.get("longitude", 0.0)
            )
            transit_2 = maps_service.calculate_transit_times(dist_2)

            # Morning Slot
            morning_cost = currency_service.convert(float(m_stop.get("price", 0.0)), "USD", currency)
            morning_slot = ActivitySlot(
                time_slot="Morning",
                time_range="09:30 - 12:30",
                title=m_stop.get("name", "Historic Morning Exploration"),
                category=m_stop.get("category", "Sightseeing"),
                description=m_stop.get("description", "Morning sightseeing at iconic heritage landmark."),
                location=f"{m_stop.get('city', target_city)}",
                latitude=m_stop.get("latitude"),
                longitude=m_stop.get("longitude"),
                estimated_cost=round(morning_cost, 2),
                duration_hrs=float(m_stop.get("visit_duration_hrs", 2.5)),
                indoor_outdoor=m_stop.get("indoor_outdoor", "Outdoor"),
                weather_suitable=not (is_rainy and m_stop.get("indoor_outdoor") == "Outdoor"),
                transit_info="Origin hotel / starting point"
            )

            # Afternoon Slot
            afternoon_cost = currency_service.convert(float(a_stop.get("price", 0.0)), "USD", currency)
            afternoon_slot = ActivitySlot(
                time_slot="Afternoon",
                time_range="13:30 - 16:30",
                title=a_stop.get("name", "Afternoon Cultural Immersion"),
                category=a_stop.get("category", "Museum"),
                description=a_stop.get("description", "Afternoon exploration of world-class cultural galleries and exhibits."),
                location=f"{a_stop.get('city', target_city)}",
                latitude=a_stop.get("latitude"),
                longitude=a_stop.get("longitude"),
                estimated_cost=round(afternoon_cost, 2),
                duration_hrs=float(a_stop.get("visit_duration_hrs", 2.5)),
                indoor_outdoor=a_stop.get("indoor_outdoor", "Indoor"),
                weather_suitable=True,
                transit_info=f"{dist_1} km from morning stop (~{transit_1['transit']} min via metro/transit)"
            )

            # Evening Slot
            evening_cost = currency_service.convert(float(e_stop.get("price", 0.0)), "USD", currency)
            evening_slot = ActivitySlot(
                time_slot="Evening",
                time_range="17:00 - 19:30",
                title=e_stop.get("name", "Sunset Vista & Leisure Walk"),
                category=e_stop.get("category", "Photography"),
                description=e_stop.get("description", "Golden hour stroll and celebrated skyline photographic views."),
                location=f"{e_stop.get('city', target_city)}",
                latitude=e_stop.get("latitude"),
                longitude=e_stop.get("longitude"),
                estimated_cost=round(evening_cost, 2),
                duration_hrs=float(e_stop.get("visit_duration_hrs", 2.0)),
                indoor_outdoor=e_stop.get("indoor_outdoor", "Outdoor"),
                weather_suitable=not (is_rainy and e_stop.get("indoor_outdoor") == "Outdoor"),
                transit_info=f"{dist_2} km (~{transit_2['walking']} min walking / {transit_2['driving']} min cab)"
            )

            # Dinner Slot
            dinner_cost = currency_service.convert(float(dinner_venue.get("avg_cost_usd", 25.0)), "USD", currency)
            dinner_slot = ActivitySlot(
                time_slot="Dinner",
                time_range="20:00 - 22:00",
                title=f"Dinner at {dinner_venue.get('name', 'Local Trattoria')}",
                category="Food & Dining",
                description=f"Enjoy authentic {dinner_venue.get('cuisine', 'local')} cuisine. Highlights: {dinner_venue.get('highlights', 'Delicious culinary dishes')}.",
                location=f"{dinner_venue.get('city', target_city)}",
                latitude=dinner_venue.get("latitude", e_stop.get("latitude")),
                longitude=dinner_venue.get("longitude", e_stop.get("longitude")),
                estimated_cost=round(dinner_cost, 2),
                duration_hrs=2.0,
                indoor_outdoor="Indoor",
                weather_suitable=True,
                transit_info="Short stroll from evening sightseeing venue"
            )

            day_cost = round(morning_cost + afternoon_cost + evening_cost + dinner_cost, 2)
            
            # Polyline coordinates for interactive map
            polyline = [
                [m_stop.get("latitude", 0.0), m_stop.get("longitude", 0.0)],
                [a_stop.get("latitude", 0.0), a_stop.get("longitude", 0.0)],
                [e_stop.get("latitude", 0.0), e_stop.get("longitude", 0.0)],
                [dinner_venue.get("latitude", e_stop.get("latitude", 0.0)), dinner_venue.get("longitude", e_stop.get("longitude", 0.0))]
            ]

            day_plan = DayPlan(
                day_number=day_num,
                title=f"Day {day_num}: {target_city} - {m_stop.get('name', 'Highlights')} & Surroundings",
                city=target_city,
                date_display=forecast.get("date", f"Day {day_num}"),
                weather_summary={
                    "condition": forecast.get("condition", "Pleasant"),
                    "temp_max": forecast.get("temp_max_c", 22),
                    "temp_min": forecast.get("temp_min_c", 14),
                    "icon": forecast.get("icon", "🌤️"),
                    "rain_probability": forecast.get("rain_probability", 10),
                    "is_rainy": is_rainy
                },
                morning=morning_slot,
                afternoon=afternoon_slot,
                evening=evening_slot,
                dinner=dinner_slot,
                day_cost_estimate=day_cost,
                route_polyline=polyline
            )
            day_plans.append(day_plan)

        return day_plans

itinerary_agent = ItineraryAgent()
