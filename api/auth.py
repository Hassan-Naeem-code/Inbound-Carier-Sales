from fastapi import APIRouter, Depends, HTTPException
from core.security import get_api_key
from services.fmcsa import FMCSAService
from pydantic import BaseModel, field_validator
from typing import Union
import logging
import json

logger = logging.getLogger(__name__)

router = APIRouter()
fmcsa_service = FMCSAService()

class MCVerificationRequest(BaseModel):
    mc_number: Union[str, int]
    
    @field_validator('mc_number', mode='before')
    @classmethod
    def convert_mc_number_to_string(cls, v):
        """Convert MC number to string regardless of input type"""
        if isinstance(v, (int, float)):
            return str(int(v))  # Convert to int first to remove decimal, then to string
        elif isinstance(v, str):
            return v.strip()  # Remove any whitespace
        else:
            raise ValueError("MC number must be a string or number")

@router.post("/verify_mc", dependencies=[Depends(get_api_key)])
def verify_mc(request: MCVerificationRequest):
    """Verify MC number using real FMCSA API"""
    try:
        # Log the incoming payload for debugging
        payload_data = {
            "original_mc_number": request.mc_number,
            "mc_number_type": type(request.mc_number).__name__,
            "raw_payload": request.dict()
        }
        logger.info(f"🔍 VERIFY_MC Request Payload: {json.dumps(payload_data, indent=2)}")
        
        # Log the processed MC number after validation
        logger.info(f"📝 Processing MC verification for: {request.mc_number}")
        
        result = fmcsa_service.verify_mc_number(request.mc_number)
        
        # Log the result summary
        logger.info(f"✅ VERIFY_MC Result: MC {request.mc_number} -> eligible: {result.get('eligible', False)}, status: {result.get('status', 'unknown')}")
        
        return result
    except ValueError as e:
        logger.error(f"❌ VERIFY_MC Validation Error: {str(e)} - Payload: {request.dict()}")
        raise HTTPException(status_code=422, detail=f"Invalid MC number format: {str(e)}")
    except Exception as e:
        logger.error(f"❌ VERIFY_MC Processing Error: {str(e)} - Payload: {request.dict()}")
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
