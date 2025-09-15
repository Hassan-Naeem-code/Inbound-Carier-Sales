import requests
import os

def verify_mc_number(mc_number: str) -> bool:
    # TODO: Replace with real FMCSA API integration
    valid_mc = {"123456", "654321"}
    return mc_number in valid_mc
