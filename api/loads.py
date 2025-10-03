from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List
import json
import os
from core.security import get_api_key

router = APIRouter()

def get_loads_data():
    """Load data from JSON file when needed"""
    try:
        data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/loads.json'))
        with open(data_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading loads data: {e}")
        return []

@router.get("/loads", dependencies=[Depends(get_api_key)])
def get_loads(equipment_type: str = None, origin: str = None, destination: str = None) -> List[dict]:
    loads = get_loads_data()
    results = loads
    if equipment_type:
        results = [l for l in results if l["equipment_type"].lower() == equipment_type.lower()]
    if origin:
        results = [l for l in results if origin.lower() in l["origin"].lower()]
    if destination:
        results = [l for l in results if destination.lower() in l["destination"].lower()]
    return results

@router.get("/load/{load_id}", dependencies=[Depends(get_api_key)])
def get_load(load_id: str):
    loads = get_loads_data()
    for l in loads:
        if l["load_id"] == load_id:
            return l
    raise HTTPException(status_code=404, detail="Load not found")

@router.post("/search_loads", dependencies=[Depends(get_api_key)])
async def search_loads(request: Request):
    """Search loads by equipment_type, origin, and destination from JSON body"""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No JSON body provided. Required keys: equipment_type, origin, destination."
        )

    required_keys = ["equipment_type", "origin", "destination"]
    missing = [k for k in required_keys if k not in body or not body[k]]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required keys: {', '.join(missing)}"
        )

    equipment_type = body.get("equipment_type")
    origin = body.get("origin")
    destination = body.get("destination")
    loads = get_loads_data()
    results = loads
    if equipment_type:
        results = [l for l in results if l["equipment_type"].lower() == equipment_type.lower()]
    if origin:
        results = [l for l in results if origin.lower() in l["origin"].lower()]
    if destination:
        results = [l for l in results if destination.lower() in l["destination"].lower()]
    return results