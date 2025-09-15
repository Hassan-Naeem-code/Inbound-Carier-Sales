from fastapi import APIRouter, Depends
from core.security import get_api_key

router = APIRouter()

@router.post("/verify_mc", dependencies=[Depends(get_api_key)])
def verify_mc(mc_number: str):
    # Placeholder for FMCSA API integration
    valid_mc = {"123456", "654321"}
    if mc_number in valid_mc:
        return {"mc_number": mc_number, "eligible": True}
    return {"mc_number": mc_number, "eligible": False}
