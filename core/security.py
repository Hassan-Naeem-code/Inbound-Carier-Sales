from fastapi import Depends, HTTPException
from fastapi.security.api_key import APIKeyHeader
from core.config import Config

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != Config.API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
