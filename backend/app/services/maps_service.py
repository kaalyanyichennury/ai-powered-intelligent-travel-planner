import math
from typing import List, Dict, Any, Tuple

class MapsService:
    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate great-circle distance between two geographic points in kilometers."""
        R = 6371.0  # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        a = (
            math.sin(d_lat / 2.0) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2.0) ** 2
        )
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
        return round(R * c, 2)

    @classmethod
    def calculate_transit_times(cls, dist_km: float) -> Dict[str, int]:
        """Calculates realistic city transit times in minutes based on distance."""
        if dist_km <= 0.05:
            return {"walking": 2, "driving": 3, "transit": 3}

        # Walking at ~4.5 km/h
        walking_mins = max(3, int(round((dist_km / 4.5) * 60)))
        
        # City driving with traffic & parking overhead (25 km/h avg)
        driving_mins = max(5, int(round((dist_km / 25.0) * 60 + 5)))

        # Metro/transit with station wait time
        transit_mins = max(8, int(round((dist_km / 28.0) * 60 + 8)))

        return {
            "walking": walking_mins,
            "driving": driving_mins,
            "transit": transit_mins
        }

    @classmethod
    def optimize_route(cls, places: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Orders a list of place dictionaries using Nearest Neighbor heuristic
        to create an efficient, logical geographic progression for the day.
        """
        if len(places) <= 2:
            return places

        unvisited = places.copy()
        ordered = [unvisited.pop(0)]  # Start with the first landmark

        while unvisited:
            last = ordered[-1]
            last_lat = last.get("latitude", 0.0)
            last_lon = last.get("longitude", 0.0)

            # Find closest unvisited place
            closest_idx = 0
            min_dist = float("inf")
            for idx, candidate in enumerate(unvisited):
                c_lat = candidate.get("latitude", 0.0)
                c_lon = candidate.get("longitude", 0.0)
                dist = cls.haversine_distance_km(last_lat, last_lon, c_lat, c_lon)
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = idx

            ordered.append(unvisited.pop(closest_idx))

        return ordered

maps_service = MapsService()
