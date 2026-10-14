from pydantic import ValidationError
from .entity_extractor import entity_extractor
from ..schemas.travel_schemas import ParsedTravelEntities
from ..services.gemini_service import GeminiError, gemini_service

class NLPParser:
    def parse_query(self, query: str) -> ParsedTravelEntities:
        """
        Parses a free-form natural language query into structured travel request parameters.
        Uses local extraction when Gemini is not configured and Gemini refinement when it is.
        """
        # First, run fast local rule & regex NLP extraction
        dest = entity_extractor.extract_destination(query) or "Paris"
        duration = entity_extractor.extract_duration(query)
        travelers = entity_extractor.extract_travelers(query)
        budget, currency = entity_extractor.extract_budget_and_currency(query)
        interests = entity_extractor.extract_interests(query)
        month = entity_extractor.extract_month(query)

        parsed = ParsedTravelEntities(
            destination=dest,
            duration_days=duration,
            travelers=travelers,
            budget=budget,
            currency=currency,
            interests=interests,
            travel_month=month,
            extraction_confidence=0.95,
            raw_query=query
        )

        if gemini_service.is_configured:
            return self._refine_with_gemini(query, parsed)

        return parsed

    def _refine_with_gemini(self, query: str, base_entities: ParsedTravelEntities) -> ParsedTravelEntities:
        parsed_data = gemini_service.generate_json(
            contents=[{"role": "user", "parts": [{"text": query}]}],
            system_instruction=(
                "Extract travel-planning details from the user's request. "
                "Return destination, duration_days (integer), travelers (integer), "
                "budget (number), currency (ISO currency code), interests (array of strings), "
                "and travel_month (month name or null). Use reasonable defaults only when "
                "the user did not specify a value: Paris, 7 days, 2 travelers, 2500 USD, "
                "history/photography/food, May."
            ),
        )
        try:
            return ParsedTravelEntities.model_validate({
                **base_entities.model_dump(),
                **parsed_data,
                "extraction_confidence": 0.99,
                "raw_query": query,
            })
        except ValidationError as exc:
            raise GeminiError("Gemini returned travel details in an invalid format.") from exc

nlp_parser = NLPParser()
