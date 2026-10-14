from fastapi import APIRouter, Query
from ..services.weather_service import weather_service
from ..services.places_service import places_service

router = APIRouter(prefix="/api/weather", tags=["Weather"])

@router.get("/")
def get_destination_weather(
    destination: str = Query("Paris", description="Destination city name"),
    days: int = Query(7, ge=1, le=14)
):
    """Fetches multi-day weather forecast with rain probability for any destination."""
    geo = places_service.geocode_destination(destination)
    forecast = weather_service.get_forecast(geo["latitude"], geo["longitude"], days=days)
    return {
        "destination": geo["city"],
        "country": geo.get("country", ""),
        "coordinates": {"lat": geo["latitude"], "lon": geo["longitude"]},
        "forecast": forecast
    }
