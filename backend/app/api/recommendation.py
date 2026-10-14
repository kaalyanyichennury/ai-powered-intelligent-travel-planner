from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel
from ..services.places_service import places_service
from ..ml.recommender import recommender
from ..ml.ranking import ranking_engine
from ..schemas.travel_schemas import PlaceSchema

router = APIRouter(prefix="/api/recommendation", tags=["Recommendations"])

class RecommendationRequest(BaseModel):
    destination: str
    interests: List[str]
    country: Optional[str] = None
    weather_rainy: Optional[bool] = False

@router.post("/", response_model=List[PlaceSchema])
def get_recommendations(req: RecommendationRequest):
    """Calculates TF-IDF + Cosine Similarity recommendations for a destination and interests."""
    places = places_service.get_attractions_for_city(req.destination, req.country)
    scored = recommender.recommend(
        places,
        user_interests=req.interests,
        top_k=20,
        weather_rainy=req.weather_rainy
    )
    ranked = ranking_engine.rerank_diverse_attractions(scored)

    return [
        PlaceSchema(
            place_id=p.get("place_id"),
            name=p.get("name"),
            city=p.get("city"),
            country=p.get("country", "Global"),
            latitude=p.get("latitude", 0.0),
            longitude=p.get("longitude", 0.0),
            category=p.get("category", "General"),
            description=p.get("description", ""),
            opening_hours=p.get("opening_hours", "09:00-18:00"),
            rating=float(p.get("rating", 4.5)),
            price=float(p.get("price", 0.0)),
            visit_duration_hrs=float(p.get("visit_duration_hrs", 2.0)),
            best_season=p.get("best_season", "All"),
            indoor_outdoor=p.get("indoor_outdoor", "Outdoor"),
            compatibility_score=float(p.get("compatibility_score", 0.85)),
            match_reasons=p.get("match_reasons", [])
        )
        for p in ranked
    ]
