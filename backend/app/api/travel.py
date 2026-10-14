import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.travel_schemas import NLPTravelRequest, ManualPlanRequest, ParsedTravelEntities, TravelPlanResponse
from ..nlp.parser import nlp_parser
from ..agents.orchestrator import travel_orchestrator
from ..database.database import get_db
from ..database.models import TripModel, AnalyticsLogModel
from ..services.currency_service import currency_service

router = APIRouter(prefix="/api/travel", tags=["Travel Planner"])

@router.post("/parse", response_model=ParsedTravelEntities)
def parse_natural_language_request(req: NLPTravelRequest):
    """Parses a free-form natural language query into structured parameters."""
    return nlp_parser.parse_query(req.query)

@router.post("/plan-nl", response_model=TravelPlanResponse)
def plan_trip_from_natural_language(req: NLPTravelRequest, db: Session = Depends(get_db)):
    """Full end-to-end Agentic AI trip generation from a natural language prompt."""
    entities = nlp_parser.parse_query(req.query)
    plan = travel_orchestrator.generate_plan(
        destination=entities.destination,
        duration_days=entities.duration_days,
        travelers=entities.travelers,
        budget=entities.budget,
        currency=entities.currency,
        interests=entities.interests,
        travel_month=entities.travel_month or "May"
    )

    # Log analytics event to DB
    try:
        budget_usd = currency_service.convert(entities.budget, entities.currency, "USD")
        log_entry = AnalyticsLogModel(
            destination=entities.destination,
            duration_days=entities.duration_days,
            budget_usd=budget_usd,
            currency=entities.currency,
            interests_str=",".join(entities.interests)
        )
        db.add(log_entry)
        db.commit()
    except Exception:
        db.rollback()

    return plan

@router.post("/plan-form", response_model=TravelPlanResponse)
def plan_trip_from_form(req: ManualPlanRequest, db: Session = Depends(get_db)):
    """Generates an end-to-end travel plan from structured form inputs."""
    plan = travel_orchestrator.generate_plan(
        destination=req.destination,
        duration_days=req.duration_days,
        travelers=req.travelers,
        budget=req.budget,
        currency=req.currency,
        interests=req.interests,
        travel_month=req.travel_month or "May",
        tier=req.accommodation_preference or "mid-range"
    )

    # Log analytics
    try:
        budget_usd = currency_service.convert(req.budget, req.currency, "USD")
        log_entry = AnalyticsLogModel(
            destination=req.destination,
            duration_days=req.duration_days,
            budget_usd=budget_usd,
            currency=req.currency,
            interests_str=",".join(req.interests)
        )
        db.add(log_entry)
        db.commit()
    except Exception:
        db.rollback()

    return plan

@router.get("/destinations")
def get_popular_destinations():
    """Returns top global destinations for quick selection."""
    return [
        {"name": "Paris", "country": "France", "tag": "Art & History", "image": "paris"},
        {"name": "Tokyo", "country": "Japan", "tag": "Culture & Modernity", "image": "tokyo"},
        {"name": "Rome", "country": "Italy", "tag": "Antiquity & Gastronomy", "image": "rome"},
        {"name": "New York", "country": "United States", "tag": "Skyline & Broadway", "image": "nyc"},
        {"name": "Dubai", "country": "United Arab Emirates", "tag": "Luxury & Dunes", "image": "dubai"},
        {"name": "Barcelona", "country": "Spain", "tag": "Architecture & Tapas", "image": "barcelona"},
        {"name": "Kyoto", "country": "Japan", "tag": "Temples & Zen Gardens", "image": "kyoto"},
        {"name": "Bali", "country": "Indonesia", "tag": "Beaches & Spiritual Terraces", "image": "bali"},
        {"name": "London", "country": "United Kingdom", "tag": "Monarchy & West End", "image": "london"}
    ]
