from fastapi import APIRouter, Depends, HTTPException
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
