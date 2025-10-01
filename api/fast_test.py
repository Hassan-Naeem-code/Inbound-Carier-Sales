from fastapi import APIRouter, Depends
from core.security import get_api_key
from pydantic import BaseModel, field_validator
from typing import Union
import time

router = APIRouter()

class MCVerificationRequest(BaseModel):
    mc_number: Union[str, int]
    
    @field_validator('mc_number', mode='before')
    @classmethod
    def convert_mc_number_to_string(cls, v):
        """Convert MC number to string regardless of input type"""
        if isinstance(v, (int, float)):
            return str(int(v))
        elif isinstance(v, str):
            return v.strip()
        else:
            raise ValueError("MC number must be a string or number")

@router.post("/verify_mc_fast", dependencies=[Depends(get_api_key)])
def verify_mc_fast(request: MCVerificationRequest):
    """Fast MC verification for testing - mocks FMCSA response"""
    mc_number = request.mc_number
    
    # Simulate some processing time
    time.sleep(0.1)
    
    # Mock responses based on MC number
    if mc_number in ["123456", "101010"]:
        return {
            "eligible": True,
            "mc_number": mc_number,
            "legal_name": "Test Carrier LLC",
            "dba_name": None,
            "operating_status": "A",
            "out_of_service_date": None,
            "status": "verified"
        }
    else:
        return {
            "eligible": False,
            "mc_number": mc_number,
            "legal_name": "Invalid Carrier",
            "dba_name": None,
            "operating_status": "I",
            "out_of_service_date": None,
            "status": "verified",
            "rejection_reason": "Operating status: I"
        }