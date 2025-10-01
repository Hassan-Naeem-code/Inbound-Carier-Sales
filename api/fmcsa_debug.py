from fastapi import APIRouter, Depends
from core.security import get_api_key
from services.fmcsa import FMCSAService
import requests

router = APIRouter()

@router.get("/fmcsa/health", dependencies=[Depends(get_api_key)])
def check_fmcsa_health():
    """Check FMCSA API health status"""
    try:
        fmcsa_service = FMCSAService()
        
        # Test with a known MC number that should work
        test_result = fmcsa_service.verify_mc_number("123456")
        
        if test_result.get("status") in ["verified", "not_found", "api_server_error", "api_unavailable"]:
            return {
                "status": "healthy",
                "fmcsa_api_status": test_result.get("status"),
                "cache_size": len(fmcsa_service._cache),
                "test_mc": "123456",
                "test_result": test_result.get("eligible", False)
            }
        else:
            return {
                "status": "degraded",
                "fmcsa_api_status": test_result.get("status"),
                "cache_size": len(fmcsa_service._cache),
                "issue": "Unexpected response format"
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "FMCSA service initialization failed"
        }

@router.get("/fmcsa/cache/stats", dependencies=[Depends(get_api_key)])
def get_cache_stats():
    """Get FMCSA cache statistics"""
    try:
        fmcsa_service = FMCSAService()
        cache_stats = {
            "cache_size": len(fmcsa_service._cache),
            "cache_ttl_seconds": fmcsa_service._cache_ttl,
            "cached_mc_numbers": list(fmcsa_service._cache.keys())[:10]  # Show first 10
        }
        return cache_stats
    except Exception as e:
        return {"error": str(e)}

@router.post("/fmcsa/cache/clear", dependencies=[Depends(get_api_key)])
def clear_cache():
    """Clear FMCSA cache"""
    try:
        fmcsa_service = FMCSAService()
        cache_size = len(fmcsa_service._cache)
        fmcsa_service._cache.clear()
        return {"message": f"Cleared {cache_size} cached entries"}
    except Exception as e:
        return {"error": str(e)}