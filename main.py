
from fastapi import FastAPI, Request
import os
import logging
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="HappyRobot Inbound Carrier API")

# Simplified request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log basic request info
    logger.info(f"📥 {request.method} {request.url.path} from {request.client.host}")
    
    response = await call_next(request)
    
    # Log response with timing
    process_time = time.time() - start_time
    logger.info(f"📤 {response.status_code} - {process_time:.2f}s")
    
    return response

# Health check endpoint for Fly.io
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
def read_root():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")

# API info endpoint
@app.get("/api_info")
def api_info():
    return {"message": "HappyRobot Inbound Carrier API", "status": "running"}

# Import routers with error handling
try:
    from api.loads import router as loads_router
    app.include_router(loads_router)
except Exception as e:
    print(f"Error loading loads router: {e}")

try:
    from api.negotiation import router as negotiation_router
    app.include_router(negotiation_router)
except Exception as e:
    print(f"Error loading negotiation router: {e}")

try:
    from api.webhook import router as webhook_router
    app.include_router(webhook_router)
except Exception as e:
    print(f"Error loading webhook router: {e}")

try:
    from api.auth import router as auth_router
    app.include_router(auth_router)
except Exception as e:
    print(f"Error loading auth router: {e}")
    
# Import dashboard view router
try:
    from api.dashboard_view import router as dashboard_router
    app.include_router(dashboard_router)
except Exception as e:
    print(f"Error loading dashboard router: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
