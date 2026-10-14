import pytest
from backend.app.agents.orchestrator import travel_orchestrator
from backend.app.agents.destination_agent import destination_agent
from backend.app.agents.budget_agent import budget_agent
from backend.app.agents.verification_agent import verification_agent

def test_destination_agent_multi_city():
    res = destination_agent.run("Italy", 7)
    assert len(res["cities"]) >= 2
    assert "Rome" in res["cities"]

def test_budget_agent():
    dummy_attractions = [{"price": 20.0}, {"price": 15.0}]
    b = budget_agent.run(
        user_budget=2500.0,
        currency="USD",
        duration_days=7,
        travelers=2,
        attractions=dummy_attractions,
        tier="mid-range"
    )
    assert b.total_estimated > 0
    assert b.user_budget == 2500.0
    assert b.status_label in ["Within Budget", "On Track (Minor variance)", "Exceeds Budget"]

def test_full_orchestration():
    plan = travel_orchestrator.generate_plan(
        destination="Paris",
        duration_days=3,
        travelers=2,
        budget=1800.0,
        currency="USD",
        interests=["History", "Food"]
    )
    assert plan.destination == "Paris"
    assert len(plan.itinerary) == 3
    assert plan.verification.score_percentage >= 80
    assert len(plan.recommended_attractions) > 0
