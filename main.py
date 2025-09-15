
from fastapi import FastAPI
from api.loads import router as loads_router
from api.negotiation import router as negotiation_router
from api.webhook import router as webhook_router
from api.auth import router as auth_router

app = FastAPI(title="HappyRobot Inbound Carrier API")

app.include_router(loads_router)
app.include_router(negotiation_router)
app.include_router(webhook_router)
app.include_router(auth_router)
