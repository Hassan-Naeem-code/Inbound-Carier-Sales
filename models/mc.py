from pydantic import BaseModel

class MCVerifyRequest(BaseModel):
    mc_number: str

class MCVerifyResponse(BaseModel):
    mc_number: str
    eligible: bool
