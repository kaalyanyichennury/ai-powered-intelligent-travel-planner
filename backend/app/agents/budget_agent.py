import logging
from typing import Dict, Any, List
from ..services.currency_service import currency_service
from ..schemas.travel_schemas import BudgetBreakdown

logger = logging.getLogger(__name__)

# Daily base costs in USD per person by tier
COST_TIERS = {
    "budget": {
        "hotel_per_night": 50.0,
        "food_per_day": 25.0,
        "transit_per_day": 8.0,
        "flight_base_pp": 320.0,
        "misc_buffer_pct": 0.05
    },
    "mid-range": {
        "hotel_per_night": 135.0,
        "food_per_day": 45.0,
        "transit_per_day": 15.0,
        "flight_base_pp": 450.0,
        "misc_buffer_pct": 0.06
    },
    "luxury": {
        "hotel_per_night": 450.0,
        "food_per_day": 120.0,
        "transit_per_day": 40.0,
        "flight_base_pp": 900.0,
        "misc_buffer_pct": 0.08
    }
}

class BudgetAgent:
    """Calculates granular multi-category trip costs and validates user budget compatibility."""
    def run(
        self,
        user_budget: float,
        currency: str,
        duration_days: int,
        travelers: int,
        attractions: List[Dict[str, Any]],
        tier: str = "mid-range"
    ) -> BudgetBreakdown:
        curr = currency.upper()
        # Convert user budget to USD to standardize calculations
        budget_usd = currency_service.convert(user_budget, curr, "USD")

        tier_config = COST_TIERS.get(tier.lower(), COST_TIERS["mid-range"])
        
        # Calculate attraction costs in USD
        activities_usd = sum([float(a.get("price", 0.0)) for a in attractions[:duration_days * 3]]) * travelers

        # Accommodation (assuming travelers share rooms if >= 2)
        rooms_needed = max(1, (travelers + 1) // 2)
        hotel_total_usd = tier_config["hotel_per_night"] * duration_days * rooms_needed

        # Flight estimate
        flights_total_usd = tier_config["flight_base_pp"] * travelers

        # Food & dining
        food_total_usd = tier_config["food_per_day"] * duration_days * travelers

        # Local transit
        transit_total_usd = tier_config["transit_per_day"] * duration_days * travelers

        # Miscellaneous & contingency
        subtotal_usd = flights_total_usd + hotel_total_usd + food_total_usd + transit_total_usd + activities_usd
        misc_usd = subtotal_usd * tier_config["misc_buffer_pct"]
        total_estimated_usd = subtotal_usd + misc_usd

        # If user budget in USD is substantially lower, scale smartly towards budget category
        if budget_usd < total_estimated_usd and tier != "budget":
            # Recalculate using budget tier
            return self.run(user_budget, currency, duration_days, travelers, attractions, tier="budget")

        # Convert all components back to user currency
        flights = currency_service.convert(flights_total_usd, "USD", curr)
        hotel = currency_service.convert(hotel_total_usd, "USD", curr)
        transit = currency_service.convert(transit_total_usd, "USD", curr)
        food = currency_service.convert(food_total_usd, "USD", curr)
        activities = currency_service.convert(activities_usd, "USD", curr)
        misc = currency_service.convert(misc_usd, "USD", curr)
        total_estimated = flights + hotel + transit + food + activities + misc

        balance = round(user_budget - total_estimated, 2)
        is_within_budget = total_estimated <= (user_budget * 1.05)  # within 5% tolerance

        if balance >= 0:
            status_label = "Within Budget"
        elif abs(balance) <= (user_budget * 0.10):
            status_label = "On Track (Minor variance)"
        else:
            status_label = "Exceeds Budget"

        symbol = currency_service.get_symbol(curr)
        rate_to_usd = currency_service.convert(1.0, "USD", curr)

        return BudgetBreakdown(
            currency=curr,
            symbol=symbol,
            user_budget=round(user_budget, 2),
            flights_estimate=round(flights, 2),
            accommodation_estimate=round(hotel, 2),
            local_transit_estimate=round(transit, 2),
            food_dining_estimate=round(food, 2),
            activities_estimate=round(activities, 2),
            miscellaneous_estimate=round(misc, 2),
            total_estimated=round(total_estimated, 2),
            balance=balance,
            is_within_budget=is_within_budget,
            status_label=status_label,
            currency_rate_to_usd=rate_to_usd
        )

budget_agent = BudgetAgent()
