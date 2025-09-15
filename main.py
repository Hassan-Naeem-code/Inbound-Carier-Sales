
from fastapi import FastAPI

app = FastAPI(title="HappyRobot Inbound Carrier API")

# Health check endpoint for Fly.io
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Root endpoint
@app.get("/")
def read_root():
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
