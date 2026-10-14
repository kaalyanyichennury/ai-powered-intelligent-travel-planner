import pytest
from backend.app.ml.recommender import recommender
from backend.app.services.places_service import places_service

def test_ml_recommender_scoring():
    places = places_service.get_attractions_for_city("Paris")
    assert len(places) > 0

    interests = ["History", "Art", "Museums"]
    recommendations = recommender.recommend(places, user_interests=interests, top_k=5)

    assert len(recommendations) > 0
    # Top pick should have high compatibility score
    top = recommendations[0]
    assert top["compatibility_score"] >= 0.70
    assert "compatibility_percentage" in top
    assert len(top["match_reasons"]) > 0

def test_ml_weather_adaptation():
    places = places_service.get_attractions_for_city("Paris")
    rec_sunny = recommender.recommend(places, user_interests=["History"], weather_rainy=False)
    rec_rainy = recommender.recommend(places, user_interests=["History"], weather_rainy=True)

    # In rainy weather, indoor places should have boosted score
    indoor_rainy = [p for p in rec_rainy if str(p.get("indoor_outdoor")).lower() == "indoor"]
    assert len(indoor_rainy) > 0
