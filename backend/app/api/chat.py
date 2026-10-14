import re
import logging
from fastapi import APIRouter
from ..schemas.travel_schemas import ChatRequest, ChatResponse, TravelPlanResponse, ActivitySlot
from ..rag.retriever import rag_retriever
from ..services.places_service import places_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["AI Travel Assistant"])

@router.post("/", response_model=ChatResponse)
def handle_chat_message(req: ChatRequest):
    """
    Intelligent Conversational Agent handling:
    1. Conversational Itinerary Modification ('replace museum on Day 2 with something outdoors')
    2. Grounded RAG Question Answering with source attribution
    """
    user_msg = req.message.strip()
    msg_lower = user_msg.lower()
    plan = req.current_plan
    destination_city = plan.cities[0] if plan and plan.cities else None

    # Check for itinerary modification intent
    is_modify = any(k in msg_lower for k in ["replace", "swap", "change", "switch", "substitute", "more outdoors", "indoor instead"])

    if is_modify and plan and plan.itinerary:
        # Detect target day
        day_match = re.search(r"day\s*(\d+)", msg_lower)
        target_day_num = int(day_match.group(1)) if day_match else 2
        
        # Clamp target day
        if target_day_num > len(plan.itinerary) or target_day_num < 1:
            target_day_num = 1

        target_day_idx = target_day_num - 1
        day_plan = plan.itinerary[target_day_idx]

        # Check if looking for outdoors
        wants_outdoors = "outdoor" in msg_lower or "park" in msg_lower or "garden" in msg_lower
        
        # Search available candidate places
        city = day_plan.city
        all_places = places_service.get_attractions_for_city(city)

        replacement = None
        if wants_outdoors:
            outdoor_candidates = [
                p for p in all_places
                if str(p.get("indoor_outdoor", "")).lower() == "outdoor"
                and p.get("name") not in [day_plan.morning.title, day_plan.afternoon.title, day_plan.evening.title]
            ]
            if outdoor_candidates:
                replacement = outdoor_candidates[0]

        if not replacement:
            # Pick any unused place
            unused = [
                p for p in all_places
                if p.get("name") not in [day_plan.morning.title, day_plan.afternoon.title, day_plan.evening.title]
            ]
            replacement = unused[0] if unused else all_places[0]

        # Determine which slot to replace (default afternoon)
        slot_to_replace = "afternoon"
        old_title = day_plan.afternoon.title
        if "morning" in msg_lower:
            slot_to_replace = "morning"
            old_title = day_plan.morning.title
        elif "evening" in msg_lower:
            slot_to_replace = "evening"
            old_title = day_plan.evening.title

        # Create new activity slot
        new_slot = ActivitySlot(
            time_slot=slot_to_replace.capitalize(),
            time_range="13:30 - 16:30" if slot_to_replace == "afternoon" else ("09:30 - 12:30" if slot_to_replace == "morning" else "17:00 - 19:30"),
            title=replacement.get("name"),
            category=replacement.get("category", "Nature"),
            description=replacement.get("description", "Picturesque leisure and cultural exploration."),
            location=city,
            latitude=replacement.get("latitude"),
            longitude=replacement.get("longitude"),
            estimated_cost=float(replacement.get("price", 0.0)),
            duration_hrs=float(replacement.get("visit_duration_hrs", 2.0)),
            indoor_outdoor=replacement.get("indoor_outdoor", "Outdoor"),
            weather_suitable=True,
            transit_info="Route recalculated to maintain optimal transit efficiency."
        )

        if slot_to_replace == "morning":
            day_plan.morning = new_slot
        elif slot_to_replace == "evening":
            day_plan.evening = new_slot
        else:
            day_plan.afternoon = new_slot

        # Update day route polyline
        day_plan.route_polyline = [
            [day_plan.morning.latitude or 0.0, day_plan.morning.longitude or 0.0],
            [day_plan.afternoon.latitude or 0.0, day_plan.afternoon.longitude or 0.0],
            [day_plan.evening.latitude or 0.0, day_plan.evening.longitude or 0.0]
        ]

        response_text = (
            f"Done! I updated **Day {target_day_num}** by replacing *{old_title}* with **{replacement.get('name')}**.\n\n"
            f"**Why this modification works:**\n"
            f"• **Category:** {replacement.get('category')} ({replacement.get('indoor_outdoor')})\n"
            f"• **Suitability:** Tailored for your interests and provides a refreshing outdoor ambiance.\n"
            f"• **Transit Feasibility:** Logically sequenced with Day {target_day_num} activities.\n"
            f"• **Budget Impact:** Entrance fee is {plan.budget_breakdown.symbol}{float(replacement.get('price', 0.0)):,.2f}."
        )

        return ChatResponse(
            response=response_text,
            rag_sources=["Itinerary Optimization Agent"],
            updated_plan=plan,
            suggested_actions=[
                f"What are the best cafes near {replacement.get('name')}?",
                "Can we add a photography spot for sunset?",
                "Tell me about public transport etiquette."
            ]
        )

    # Otherwise, execute grounded RAG Q&A
    rag_result = rag_retriever.answer_question(
        user_msg,
        city_context=destination_city,
        conversation_history=req.conversation_history,
    )

    return ChatResponse(
        response=rag_result["answer"],
        rag_sources=rag_result.get("sources", []),
        suggested_actions=[
            f"What is the best time to visit {destination_city or 'the city'}?",
            f"Show top food recommendations in {destination_city or 'the city'}",
            "Can you adjust Day 1 activities?"
        ]
    )
