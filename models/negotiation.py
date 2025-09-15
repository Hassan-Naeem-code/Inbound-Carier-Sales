from pydantic import BaseModel
from typing import List, Optional

class NegotiationLog(BaseModel):
    mc_number: str
    load_id: str
    accepted: bool
    final_rate: Optional[float]
    history: List[dict]
    outcome: str
    sentiment: str
