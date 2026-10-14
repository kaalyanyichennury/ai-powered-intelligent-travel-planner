import pytest
from backend.app.nlp.entity_extractor import entity_extractor
from backend.app.nlp.parser import nlp_parser

def test_extract_destination():
    dest = entity_extractor.extract_destination("Plan a 7-day trip to Paris for 2 people")
    assert dest == "Paris"

    dest_japan = entity_extractor.extract_destination("I want to visit Japan for 10 days in April")
    assert dest_japan == "Japan"

def test_extract_duration():
    assert entity_extractor.extract_duration("Plan a 7-day trip") == 7
    assert entity_extractor.extract_duration("10 days in April") == 10
    assert entity_extractor.extract_duration("for 2 weeks") == 14

def test_extract_budget_and_currency():
    b1, c1 = entity_extractor.extract_budget_and_currency("budget of $2,500")
    assert b1 == 2500.0
    assert c1 == "USD"

    b2, c2 = entity_extractor.extract_budget_and_currency("budget of ₹1.5 lakh")
    assert b2 == 150000.0
    assert c2 == "INR"

    b3, c3 = entity_extractor.extract_budget_and_currency("budget of €1,800")
    assert b3 == 1800.0
    assert c3 == "EUR"

def test_full_nlp_parser():
    res = nlp_parser.parse_query("Plan a 7-day trip to Paris for 2 people with a budget of $2,500. I like history, photography and food.")
    assert res.destination == "Paris"
    assert res.duration_days == 7
    assert res.travelers == 2
    assert res.budget == 2500.0
    assert res.currency == "USD"
    assert "History" in res.interests
