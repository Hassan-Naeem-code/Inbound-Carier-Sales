from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security.api_key import APIKeyHeader
from typing import List
import json
import os
from agent import CarrierAgent

API_KEY = os.getenv("API_KEY", "test-api-key")
api_key_header = APIKeyHeader(name="X-API-Key")

app = FastAPI(title="HappyRobot Inbound Carrier API")

# Load data from JSON
with open("loads.json") as f:
    LOADS = json.load(f)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.get("/loads", dependencies=[Depends(get_api_key)])
def get_loads(equipment_type: str = None, origin: str = None, destination: str = None) -> List[dict]:
    results = LOADS
    if equipment_type:
        results = [l for l in results if l["equipment_type"].lower() == equipment_type.lower()]
    if origin:
        results = [l for l in results if origin.lower() in l["origin"].lower()]
    if destination:
        results = [l for l in results if destination.lower() in l["destination"].lower()]
    return results

@app.get("/load/{load_id}", dependencies=[Depends(get_api_key)])
def get_load(load_id: str):
    for l in LOADS:
        if l["load_id"] == load_id:
            return l
    raise HTTPException(status_code=404, detail="Load not found")

@app.post("/verify_mc", dependencies=[Depends(get_api_key)])
def verify_mc(mc_number: str):
    # Placeholder for FMCSA API integration
    # Simulate valid MC numbers for demo
    valid_mc = {"123456", "654321"}
    if mc_number in valid_mc:
        return {"mc_number": mc_number, "eligible": True}
    return {"mc_number": mc_number, "eligible": False}

@app.post("/log_negotiation", dependencies=[Depends(get_api_key)])
def log_negotiation(data: dict):
    # For demo, just print or append to a file
    with open("negotiations.log", "a") as f:
        f.write(json.dumps(data) + "\n")
    return {"status": "logged"}

@app.get("/metrics", dependencies=[Depends(get_api_key)])
def get_metrics():
    # Demo: count negotiations
    try:
        with open("negotiations.log") as f:
            lines = f.readlines()
        return {"negotiations": len(lines)}
    except FileNotFoundError:
        return {"negotiations": 0}

# Webhook endpoint for HappyRobot web call trigger
@app.post("/webhook/happyrobot")
async def happyrobot_webhook(payload: dict):
    """
    Expects payload with keys: mc_number, equipment_type, origin, destination, initial_offer, call_transcript
    """
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
    return {
        "status": "processed",
        "load": chosen_load,
        "negotiation": negotiation,
        "outcome": outcome,
        "sentiment": sentiment
    }

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
