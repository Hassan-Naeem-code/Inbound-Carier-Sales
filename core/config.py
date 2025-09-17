"""
Environment Configuration Module
Centralized configuration management for HappyRobot Inbound Carrier API
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration class"""
    
    # API Configuration
    API_KEY = os.getenv("API_KEY")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    PORT = int(os.getenv("PORT", 8000))
    
    # FMCSA Integration
    FMCSA_API_TOKEN = os.getenv("FMCSA_API_TOKEN")
    FMCSA_BASE_URL = "https://mobile.fmcsa.dot.gov/qc/services/carriers"
    
    # Application Settings
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Validation
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required_vars = {
            "API_KEY": cls.API_KEY,
            "FMCSA_API_TOKEN": cls.FMCSA_API_TOKEN
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please check your .env file or environment configuration."
            )
    
    @classmethod
    def is_production(cls):
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == "production"
    
    @classmethod
    def is_development(cls):
        """Check if running in development environment"""
        return cls.ENVIRONMENT.lower() == "development"

# Legacy Settings class for backward compatibility
class Settings:
    API_KEY: str = Config.API_KEY

settings = Settings()

# Initialize and validate configuration
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration Error: {e}")
    if Config.is_development():
        print("Please copy .env.example to .env and update with your credentials")
    raise
