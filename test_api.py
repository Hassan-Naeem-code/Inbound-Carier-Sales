"""
Basic tests for HappyRobot Inbound Carrier API
"""
import pytest
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set up test environment
os.environ["API_KEY"] = "test-api-key"
os.environ["FMCSA_API_TOKEN"] = "test-token"
os.environ["ENVIRONMENT"] = "testing"

from main import app

client = TestClient(app)

def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "running"

def test_loads_endpoint_without_auth():
    """Test loads endpoint without authentication"""
    response = client.get("/loads")
    assert response.status_code == 422  # Unprocessable Entity (missing API key)

def test_loads_endpoint_with_auth():
    """Test loads endpoint with authentication"""
    headers = {"X-API-Key": "test-api-key"}
    response = client.get("/loads", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_loads_endpoint_invalid_auth():
    """Test loads endpoint with invalid API key"""
    headers = {"X-API-Key": "invalid-key"}
    response = client.get("/loads", headers=headers)
    assert response.status_code == 403

def test_webhook_endpoint():
    """Test the webhook endpoint"""
    with patch('services.fmcsa.FMCSAService.verify_mc_number') as mock_verify:
        # Mock FMCSA service to avoid actual API calls in tests
        mock_verify.return_value = {
            "eligible": False,
            "mc_number": "123456",
            "status": "not_found",
            "message": "MC number not found in FMCSA database"
        }
        
        payload = {
            "mc_number": "123456",
            "equipment_type": "Dry Van",
            "origin": "Chicago, IL",
            "destination": "Dallas, TX",
            "initial_offer": 2100,
            "call_transcript": "Hello, I am interested in your load"
        }
        
        response = client.post("/webhook/happyrobot", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "rejected"
        assert data["reason"] == "MC not eligible"

def test_config_validation():
    """Test that configuration loads properly"""
    from core.config import Config
    assert Config.API_KEY == "test-api-key"
    assert Config.FMCSA_API_TOKEN == "test-token"
    assert Config.ENVIRONMENT == "testing"

def test_fmcsa_service_initialization():
    """Test FMCSA service can be initialized"""
    from services.fmcsa import FMCSAService
    service = FMCSAService()
    assert service.api_token == "test-token"
    assert service.base_url == "https://mobile.fmcsa.dot.gov/qc/services/carriers"

if __name__ == "__main__":
    pytest.main([__file__])