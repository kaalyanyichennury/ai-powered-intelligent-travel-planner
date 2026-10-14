import uuid
import logging
from typing import Dict, Any, List
from ..schemas.travel_schemas import TravelPlanResponse, PlaceSchema
from .destination_agent import destination_agent
from .weather_agent import weather_agent
from .recommendation_agent import recommendation_agent
from .budget_agent import budget_agent
from .itinerary_agent import itinerary_agent
from .verification_agent import verification_agent
from ..rag.retriever import rag_retriever

logger = logging.getLogger(__name__)

class TravelOrchestrator:
    """Master orchestrator executing the full multi-agent travel planning pipeline."""
    def generate_plan(
        self,
        destination: str,
        duration_days: int = 7,
        travelers: int = 2,
        budget: float = 2500.0,
        currency: str = "USD",
        interests: List[str] = None,
        travel_month: str = "May",
        tier: str = "mid-range"
    ) -> TravelPlanResponse:
        interests = interests or ["History", "Photography", "Food"]
        trip_id = f"trip_{uuid.uuid4().hex[:8]}"
        logger.info(f"Orchestrating trip plan {trip_id} for {destination} ({duration_days} days, {currency} {budget})")

        # Step 1: Destination Agent
        dest_result = destination_agent.run(destination, duration_days)
        cities = dest_result["cities"]
        country = dest_result["country"]
        cities_detail = dest_result["cities_detail"]

        # Step 2: Weather Agent
        weather_result = weather_agent.run(cities_detail, duration_days)

        # Step 3: Recommendation Agent (ML Engine)
        rec_result = recommendation_agent.run(
            cities=cities,
            interests=interests,
            country=country,
            weather_advisory=weather_result
        )
        ranked_attractions = rec_result["all_ranked_attractions"]

        # Step 4: Budget Agent
        budget_breakdown = budget_agent.run(
            user_budget=budget,
            currency=currency,
            duration_days=duration_days,
            travelers=travelers,
            attractions=ranked_attractions,
            tier=tier
        )

        # Step 5: Itinerary Agent
        daily_plans = itinerary_agent.run(
            cities_detail=cities_detail,
            attractions=ranked_attractions,
            weather_data=weather_result,
            currency=currency,
            total_days=duration_days
        )

        # Step 6: Verification Agent
        verification_summary = verification_agent.run(
            itinerary=daily_plans,
            budget_breakdown=budget_breakdown,
            user_budget=budget,
            weather_advisory=weather_result
        )

        # Step 7: RAG System Insights
        rag_answer = rag_retriever.answer_question(
            f"What are essential travel rules, cultural tips and best photo spots for {cities[0]}?",
            city_context=cities[0]
        )
        rag_tips = [
            {"title": "Destination Insight", "content": rag_answer["answer"]},
            {"title": "Weather Outlook", "content": "; ".join(weather_result.get("advisories", []))}
        ]

        # Convert top attractions to schema
        attraction_schemas = [
            PlaceSchema(
                place_id=p.get("place_id"),
                name=p.get("name"),
                city=p.get("city"),
                country=p.get("country", country),
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
            for p in ranked_attractions[:10]
        ]

        overview = (
            f"Custom {duration_days}-day itinerary across {', '.join(cities)} tailored for {travelers} traveler(s). "
            f"Featuring {len(attraction_schemas)} top-rated attractions, localized cuisine, and full geographic transit optimization."
        )

        return TravelPlanResponse(
            trip_id=trip_id,
            destination=destination,
            country=country,
            duration_days=duration_days,
            travelers=travelers,
            user_budget=budget,
            currency=currency,
            interests=interests,
            cities=cities,
            overview_description=overview,
            budget_breakdown=budget_breakdown,
            itinerary=daily_plans,
            recommended_attractions=attraction_schemas,
            verification=verification_summary,
            rag_tips=rag_tips
        )

travel_orchestrator = TravelOrchestrator()
