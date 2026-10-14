from typing import Dict, Any, List
from ..services.places_service import places_service
from ..ml.recommender import recommender
from ..ml.ranking import ranking_engine

class RecommendationAgent:
    """Invokes ML ranking to select and score destination attractions according to user interests."""
    def run(
        self,
        cities: List[str],
        interests: List[str],
        country: str = None,
        weather_advisory: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        all_city_places: List[Dict[str, Any]] = []
        is_generally_rainy = bool(weather_advisory and weather_advisory.get("rainy_days"))

        for city in cities:
            places = places_service.get_attractions_for_city(city, country)
            all_city_places.extend(places)

        # Run TF-IDF + Cosine Similarity Recommender
        scored_places = recommender.recommend(
            all_city_places,
            user_interests=interests,
            top_k=25,
            weather_rainy=is_generally_rainy
        )

        # Apply multi-criteria diversity reranking
        ranked_places = ranking_engine.rerank_diverse_attractions(scored_places)

        return {
            "all_ranked_attractions": ranked_places,
            "top_highlights": ranked_places[:6]
        }

recommendation_agent = RecommendationAgent()
