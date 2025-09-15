import os

class Settings:
    API_KEY: str = os.getenv("API_KEY", "test-api-key")

settings = Settings()
