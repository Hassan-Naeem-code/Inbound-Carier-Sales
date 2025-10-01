from fastapi import APIRouter
from agent import CarrierAgent
import logging
import json

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook/happyrobot")
async def happyrobot_webhook(payload: dict):
    # Log the complete incoming payload for debugging
    logger.info(f"🚀 WEBHOOK Request Payload: {json.dumps(payload, indent=2)}")
    
    agent = CarrierAgent()
    
    # Convert MC number to string if it's a number
    mc_number = payload.get("mc_number")
    original_mc_number = mc_number  # Keep original for logging
    
    if isinstance(mc_number, (int, float)):
        mc_number = str(int(mc_number))
        logger.info(f"🔄 Converted MC number from {type(original_mc_number).__name__} ({original_mc_number}) to string ({mc_number})")
    elif isinstance(mc_number, str):
        mc_number = mc_number.strip()
        if mc_number != original_mc_number:
            logger.info(f"🔄 Trimmed MC number from '{original_mc_number}' to '{mc_number}'")
    
    equipment_type = payload.get("equipment_type")
    origin = payload.get("origin")
    destination = payload.get("destination")
    initial_offer = payload.get("initial_offer")
    call_transcript = payload.get("call_transcript", "")

    logger.info(f"🔍 Verifying MC number: {mc_number}")
    mc_status = agent.verify_mc(mc_number)
    logger.info(f"✅ MC Verification Result: {json.dumps(mc_status, indent=2)}")
    
    if not mc_status.get("eligible"):
        rejection_response = {"status": "rejected", "reason": "MC not eligible", "mc_details": mc_status}
        logger.info(f"❌ WEBHOOK Result: {json.dumps(rejection_response, indent=2)}")
        return rejection_response

    logger.info(f"🚛 Searching loads: equipment={equipment_type}, origin={origin}, destination={destination}")
    loads = agent.search_loads(equipment_type=equipment_type, origin=origin, destination=destination)
    if not loads:
        no_loads_response = {"status": "no_loads_found", "search_criteria": {"equipment_type": equipment_type, "origin": origin, "destination": destination}}
        logger.info(f"📭 WEBHOOK Result: {json.dumps(no_loads_response, indent=2)}")
        return no_loads_response
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
    
    final_response = {
        "status": "processed",
        "load": chosen_load,
        "negotiation": negotiation,
        "outcome": outcome,
        "sentiment": sentiment,
        "transfer_to_sales_rep": transfer_to_sales_rep
    }
    
    logger.info(f"🎉 WEBHOOK Final Result: {json.dumps(final_response, indent=2)}")
    return final_response
