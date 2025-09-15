from fastapi import APIRouter
from agent import CarrierAgent

router = APIRouter()

@router.post("/webhook/happyrobot")
async def happyrobot_webhook(payload: dict):
    agent = CarrierAgent()
    mc_number = payload.get("mc_number")
    equipment_type = payload.get("equipment_type")
    origin = payload.get("origin")
    destination = payload.get("destination")
    initial_offer = payload.get("initial_offer")
    call_transcript = payload.get("call_transcript", "")

    mc_status = agent.verify_mc(mc_number)
    if not mc_status.get("eligible"):
        return {"status": "rejected", "reason": "MC not eligible"}

    loads = agent.search_loads(equipment_type=equipment_type, origin=origin, destination=destination)
    if not loads:
        return {"status": "no_loads_found"}
    chosen_load = loads[0]
    negotiation = agent.negotiate(chosen_load, initial_offer=initial_offer)
    outcome = agent.classify_outcome(negotiation)
    sentiment = agent.classify_sentiment(call_transcript)
    log_data = {
        "mc_number": mc_number,
        "load_id": chosen_load["load_id"],
        **negotiation,
        "outcome": outcome,
        "sentiment": sentiment
    }
    agent.log_negotiation(log_data)
    transfer_to_sales_rep = outcome == "Deal Closed"
    return {
        "status": "processed",
        "load": chosen_load,
        "negotiation": negotiation,
        "outcome": outcome,
        "sentiment": sentiment,
        "transfer_to_sales_rep": transfer_to_sales_rep
    }
