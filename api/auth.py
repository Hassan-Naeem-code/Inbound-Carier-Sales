from fastapi import APIRouter, Depends, HTTPException
from core.security import get_api_key
from services.fmcsa import FMCSAService
from pydantic import BaseModel

router = APIRouter()
fmcsa_service = FMCSAService()

class MCVerificationRequest(BaseModel):
    mc_number: str

@router.post("/verify_mc", dependencies=[Depends(get_api_key)])
def verify_mc(request: MCVerificationRequest):
    """Verify MC number using real FMCSA API"""
    try:
        result = fmcsa_service.verify_mc_number(request.mc_number)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MC verification failed: {str(e)}")

@router.get("/carrier/{mc_number}/safety-rating", dependencies=[Depends(get_api_key)])
def get_carrier_safety_rating(mc_number: str):
    """Get carrier safety rating from FMCSA"""
    try:
        safety_rating = fmcsa_service.get_carrier_safety_rating(mc_number)
        return {
            "mc_number": mc_number,
            "safety_rating": safety_rating
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get safety rating: {str(e)}")
