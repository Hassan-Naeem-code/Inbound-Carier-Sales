from pydantic import BaseModel
from typing import Optional, List

class Load(BaseModel):
    load_id: str
    origin: str
    destination: str
    pickup_datetime: str
    delivery_datetime: str
    equipment_type: str
    loadboard_rate: float
    notes: Optional[str]
    weight: float
    commodity_type: str
    num_of_pieces: int
    miles: float
    dimensions: str

class NegotiationLog(BaseModel):
    mc_number: str
    load_id: str
    accepted: bool
    final_rate: Optional[float]
    history: List[dict]
    outcome: str
    sentiment: str

class MCVerifyRequest(BaseModel):
    mc_number: str

class MCVerifyResponse(BaseModel):
    mc_number: str
    eligible: bool
