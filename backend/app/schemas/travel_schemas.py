from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class NLPTravelRequest(BaseModel):
    query: str = Field(..., json_schema_extra={"example": "Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food."})

class ParsedTravelEntities(BaseModel):
    destination: str = "Paris"
    duration_days: int = 7
    travelers: int = 2
    budget: float = 2500.0
    currency: str = "USD"
    interests: List[str] = ["history", "photography", "food"]
    travel_month: Optional[str] = "May"
    origin_city: Optional[str] = None
    extraction_confidence: float = 0.95
    raw_query: Optional[str] = None

class ManualPlanRequest(BaseModel):
    destination: str
    duration_days: int = 7
    travelers: int = 2
    budget: float = 2500.0
    currency: str = "USD"
    interests: List[str] = ["History", "Photography", "Food"]
    travel_month: Optional[str] = "May"
    accommodation_preference: Optional[str] = "mid-range"  # budget, mid-range, luxury
    pace: Optional[str] = "balanced"  # relaxed, balanced, intensive

class PlaceSchema(BaseModel):
    place_id: Optional[str] = None
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
    category: str
    description: str
    opening_hours: str = "09:00-18:00"
    rating: float = 4.5
    price: float = 0.0
    visit_duration_hrs: float = 2.0
    best_season: Optional[str] = "All"
    indoor_outdoor: str = "Outdoor"
    compatibility_score: Optional[float] = 0.85
    match_reasons: Optional[List[str]] = []

class RouteSegment(BaseModel):
    from_place: str
    to_place: str
    distance_km: float
    walking_mins: int
    driving_mins: int
    transit_mins: int

class ActivitySlot(BaseModel):
    time_slot: str  # Morning, Afternoon, Evening, Dinner
    time_range: str  # e.g., "09:30 - 12:00"
    title: str
    category: str
    description: str
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    estimated_cost: float = 0.0
    duration_hrs: float = 2.0
    indoor_outdoor: str = "Outdoor"
    weather_suitable: bool = True
    transit_info: Optional[str] = None

class DayPlan(BaseModel):
    day_number: int
    title: str
    city: str
    date_display: Optional[str] = None
    weather_summary: Optional[Dict[str, Any]] = None
    morning: ActivitySlot
    afternoon: ActivitySlot
    evening: ActivitySlot
    dinner: ActivitySlot
    day_cost_estimate: float = 0.0
    route_polyline: Optional[List[List[float]]] = []

class BudgetBreakdown(BaseModel):
    currency: str = "USD"
    symbol: str = "$"
    user_budget: float
    flights_estimate: float
    accommodation_estimate: float
    local_transit_estimate: float
    food_dining_estimate: float
    activities_estimate: float
    miscellaneous_estimate: float
    total_estimated: float
    balance: float  # user_budget - total_estimated
    is_within_budget: bool
    status_label: str  # "Under Budget", "On Track", "Exceeds Budget"
    currency_rate_to_usd: float = 1.0

class VerificationCheckItem(BaseModel):
    name: str
    passed: bool
    details: str
    severity: str = "info"  # success, warning, info

class VerificationSummary(BaseModel):
    overall_status: str  # "VERIFIED_OPTIMAL", "VERIFIED_ADJUSTED", "WARNING"
    score_percentage: int = 95
    checks: List[VerificationCheckItem] = []
    adjustments_made: List[str] = []

class TravelPlanResponse(BaseModel):
    trip_id: str
    destination: str
    country: Optional[str] = None
    duration_days: int
    travelers: int
    user_budget: float
    currency: str
    interests: List[str]
    cities: List[str]
    overview_description: str
    budget_breakdown: BudgetBreakdown
    itinerary: List[DayPlan]
    recommended_attractions: List[PlaceSchema]
    verification: VerificationSummary
    rag_tips: List[Dict[str, str]] = []
    created_at: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    current_plan: Optional[TravelPlanResponse] = None

class ChatResponse(BaseModel):
    response: str
    rag_sources: Optional[List[str]] = []
    updated_plan: Optional[TravelPlanResponse] = None
    suggested_actions: Optional[List[str]] = []

class TripSaveRequest(BaseModel):
    title: str
    destination: str
    plan_data: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    total_trips_planned: int
    top_destinations: List[Dict[str, Any]]
    top_interest_categories: List[Dict[str, Any]]
    average_trip_budget_usd: float
    popular_durations: List[Dict[str, Any]]
