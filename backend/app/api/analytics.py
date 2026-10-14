import json
import logging
from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.database import get_db
from ..database.models import TripModel, AnalyticsLogModel
from ..schemas.travel_schemas import TripSaveRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Analytics & Saved Trips"])

# Seed starter analytics data if table is fresh
STARTER_LOGS = [
    ("Paris", 7, 2450.0, "USD", "History,Food,Photography"),
    ("Tokyo", 10, 2100.0, "USD", "Anime,Temples,Food,Photography"),
    ("Rome", 5, 1800.0, "USD", "History,Architecture,Food"),
    ("New York", 4, 2200.0, "USD", "Skyline,Broadway,Shopping"),
    ("Dubai", 6, 3100.0, "USD", "Luxury,Adventure,Shopping"),
    ("Barcelona", 7, 1950.0, "USD", "Architecture,Tapas,Beach"),
    ("Kyoto", 8, 2300.0, "USD", "Temples,Gardens,Culture"),
    ("Paris", 5, 1900.0, "USD", "Art,Museums,Dining"),
    ("Tokyo", 7, 2600.0, "USD", "Tech,Food,Nightlife")
]

def ensure_starter_analytics(db: Session):
    count = db.query(AnalyticsLogModel).count()
    if count == 0:
        for dest, days, b_usd, curr, interests in STARTER_LOGS:
            db.add(AnalyticsLogModel(
                destination=dest,
                duration_days=days,
                budget_usd=b_usd,
                currency=curr,
                interests_str=interests
            ))
        db.commit()

@router.get("/analytics/dashboard")
def get_analytics_dashboard(db: Session = Depends(get_db)):
    """Computes Data Science analytics metrics over all generated trips and searches."""
    ensure_starter_analytics(db)
    logs = db.query(AnalyticsLogModel).all()
    total_trips = len(logs)

    # Destination counts
    dest_counts = Counter([l.destination for l in logs])
    popular_destinations = [
        {"destination": dest, "trips_count": count}
        for dest, count in dest_counts.most_common(6)
    ]

    # Category popularity
    all_interests = []
    for l in logs:
        if l.interests_str:
            all_interests.extend([i.strip().title() for i in l.interests_str.split(",") if i.strip()])
    category_counts = Counter(all_interests)
    top_categories = [
        {"category": cat, "count": cnt, "percentage": round((cnt / max(1, len(all_interests))) * 100, 1)}
        for cat, cnt in category_counts.most_common(7)
    ]

    # Average Budget
    budgets = [l.budget_usd for l in logs if l.budget_usd]
    avg_budget = round(sum(budgets) / len(budgets), 2) if budgets else 2250.0

    # Duration Distribution
    duration_counts = Counter([f"{l.duration_days} Days" for l in logs])
    popular_durations = [{"duration": k, "count": v} for k, v in duration_counts.most_common(5)]

    return {
        "total_trips_planned": total_trips + db.query(TripModel).count(),
        "average_trip_budget_usd": avg_budget,
        "top_destinations": popular_destinations,
        "top_categories": top_categories,
        "popular_durations": popular_durations
    }

@router.post("/trips/save")
def save_trip_plan(req: TripSaveRequest, db: Session = Depends(get_db)):
    """Saves a generated itinerary to SQLite database."""
    trip_id = req.plan_data.get("trip_id") or f"saved_{req.destination.lower()}"
    existing = db.query(TripModel).filter(TripModel.trip_id == trip_id).first()
    
    plan_json = json.dumps(req.plan_data)
    if existing:
        existing.title = req.title
        existing.plan_json = plan_json
        db.commit()
        return {"status": "updated", "trip_id": trip_id}
    else:
        new_trip = TripModel(
            trip_id=trip_id,
            title=req.title,
            destination=req.destination,
            country=req.plan_data.get("country"),
            duration_days=req.plan_data.get("duration_days", 7),
            travelers=req.plan_data.get("travelers", 2),
            budget=req.plan_data.get("user_budget", 2500.0),
            currency=req.plan_data.get("currency", "USD"),
            plan_json=plan_json
        )
        db.add(new_trip)
        db.commit()
        return {"status": "saved", "trip_id": trip_id}

@router.get("/trips")
def list_saved_trips(db: Session = Depends(get_db)):
    """Lists all saved trips from the database."""
    trips = db.query(TripModel).order_by(TripModel.created_at.desc()).all()
    results = []
    for t in trips:
        try:
            parsed = json.loads(t.plan_json)
        except Exception:
            parsed = {}
        results.append({
            "id": t.id,
            "trip_id": t.trip_id,
            "title": t.title,
            "destination": t.destination,
            "country": t.country,
            "duration_days": t.duration_days,
            "travelers": t.travelers,
            "budget": t.budget,
            "currency": t.currency,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "plan_data": parsed
        })
    return results

@router.delete("/trips/{trip_id}")
def delete_saved_trip(trip_id: str, db: Session = Depends(get_db)):
    """Deletes a saved trip from SQLite."""
    trip = db.query(TripModel).filter(TripModel.trip_id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    db.delete(trip)
    db.commit()
    return {"status": "deleted", "trip_id": trip_id}
