from fastapi import APIRouter, Depends, HTTPException, Request, status
from core.security import get_api_key
import os
import json
import logging
from pydantic import BaseModel
from typing import Optional, List

logger = logging.getLogger(__name__)
router = APIRouter()

class NegotiationRequest(BaseModel):
    load_id: str
    loadboard_rate: int
    initial_offer: int
    max_rounds: Optional[int] = 3

class NegotiationRound(BaseModel):
    round: int
    carrier_offer: int
    broker_offer: int

class NegotiationResponse(BaseModel):
    accepted: bool
    final_rate: Optional[int] = None
    history: List[dict]

@router.post("/log_negotiation", dependencies=[Depends(get_api_key)])
def log_negotiation(data: dict):
    with open(os.path.join(os.path.dirname(__file__), '../data/negotiations.log'), "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"status": "logged"}

@router.get("/metrics", dependencies=[Depends(get_api_key)])
def get_metrics():
    try:
        with open(os.path.join(os.path.dirname(__file__), '../data/negotiations.log')) as f:
            lines = f.readlines()
        return {"negotiations": len(lines)}
    except FileNotFoundError:
        return {"negotiations": 0}

@router.post("/negotiate", dependencies=[Depends(get_api_key)], response_model=NegotiationResponse)
async def negotiate(request: Request):
    """
    Handle load rate negotiation between carrier and broker
    
    Accepts:
    - load_id: ID of the load being negotiated
    - loadboard_rate: Current broker's rate for the load
    - initial_offer: Carrier's initial offer
    - max_rounds: Maximum number of negotiation rounds (default: 3)
    
    Returns:
    - accepted: Whether the negotiation was successful
    - final_rate: The final agreed rate (if accepted)
    - history: History of negotiation rounds
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No JSON body provided. Required keys: load_id, loadboard_rate, initial_offer"
        )

    required_keys = ["load_id", "loadboard_rate", "initial_offer"]
    missing = [k for k in required_keys if k not in body]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required keys: {', '.join(missing)}"
        )
    
    load_id = body.get("load_id")
    loadboard_rate = body.get("loadboard_rate")
    initial_offer = body.get("initial_offer")
    max_rounds = body.get("max_rounds", 3)
    
    # Convert values to integers if needed
    try:
        loadboard_rate = int(loadboard_rate)
        initial_offer = int(initial_offer)
        max_rounds = int(max_rounds)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="loadboard_rate, initial_offer, and max_rounds must be numeric values"
        )

    # Implement negotiation logic
    counter = loadboard_rate
    rounds = 0
    accepted = False
    negotiation_history = []
    
    logger.info(f"🤝 Starting negotiation for load {load_id}: initial offer={initial_offer}, loadboard rate={loadboard_rate}")
    
    while rounds < max_rounds:
        negotiation_history.append({
            "round": rounds+1, 
            "carrier_offer": initial_offer, 
            "broker_offer": counter
        })
        
        logger.info(f"🔄 Round {rounds+1}: carrier offered {initial_offer}, broker offered {counter}")
        
        # Accept if close enough (within $100)
        if abs(initial_offer - counter) <= 100:
            accepted = True
            logger.info(f"✅ Negotiation accepted: final rate={counter}")
            break
        
        # Calculate counter offer - midpoint between current offers
        counter = int((counter + initial_offer) / 2)
        rounds += 1
    
    if not accepted:
        logger.info(f"❌ Negotiation failed after {max_rounds} rounds")
    
    result = {
        "accepted": accepted, 
        "final_rate": counter if accepted else None, 
        "history": negotiation_history
    }
    
    # Automatically log successful negotiations
    if accepted:
        log_data = {
            "load_id": load_id,
            "initial_offer": body.get("initial_offer"),
            "final_rate": counter,
            "rounds": rounds + 1
        }
        log_negotiation(log_data)
    
    return result
