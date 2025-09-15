from fastapi import APIRouter, Depends
from core.security import get_api_key
import os
import json

router = APIRouter()

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
