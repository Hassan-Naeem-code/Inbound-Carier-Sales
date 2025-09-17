import os
from services.fmcsa import FMCSAService

# Load environment variables if using python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

service = FMCSAService()

# Test with a valid MC number
mc_number = "212121"  # You can change this to any MC number you want to test
result = service.verify_mc_number(mc_number)
print("FMCSA Verification Result:", result)