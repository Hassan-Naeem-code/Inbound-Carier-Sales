import requests
import os
from textblob import TextBlob
from services.fmcsa import FMCSAService
from core.config import Config

API_URL = Config.API_URL
HEADERS = {"X-API-Key": Config.API_KEY}

class CarrierAgent:
    def __init__(self):
        self.negotiation_log = []
        self.fmcsa_service = FMCSAService()

    def verify_mc(self, mc_number):
        """Verify MC number using real FMCSA API"""
        try:
            # Use the enhanced FMCSA service
            result = self.fmcsa_service.verify_mc_number(mc_number)
            return result
        except Exception as e:
            # Fallback to API endpoint if direct service fails
            try:
                resp = requests.post(f"{API_URL}/verify_mc", json={"mc_number": mc_number}, headers=HEADERS, timeout=10)
                return resp.json()
            except:
                return {
                    "eligible": False,
                    "mc_number": mc_number,
                    "status": "error",
                    "message": f"Verification failed: {str(e)}"
                }

    def search_loads(self, equipment_type=None, origin=None, destination=None):
        # Directly import and call the loads logic to avoid HTTP self-call deadlock
        try:
            from api.loads import get_loads
            # get_loads returns a list of dicts
            return get_loads(equipment_type=equipment_type, origin=origin, destination=destination)
        except Exception as e:
            print(f"Failed to get loads directly: {e}")
            return []

    def negotiate(self, load, initial_offer, max_rounds=3):
        """
        Negotiate a load rate by calling the negotiation API endpoint
        
        Args:
            load (dict): The load information including loadboard_rate
            initial_offer: The carrier's initial offer
            max_rounds (int): Maximum number of negotiation rounds
            
        Returns:
            dict: Negotiation result with accepted status, final rate, and history
        """
        try:
            # Try using the dedicated negotiation API endpoint
            payload = {
                "load_id": load["load_id"],
                "loadboard_rate": load["loadboard_rate"],
                "initial_offer": initial_offer,
                "max_rounds": max_rounds
            }
            
            response = requests.post(
                f"{API_URL}/negotiate", 
                json=payload, 
                headers=HEADERS, 
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Negotiation API failed with status {response.status_code}: {response.text}")
                # Fall back to local implementation
        except Exception as e:
            print(f"Failed to use negotiation API: {e}")
            # Fall back to local implementation
        
        # Fallback negotiation logic (if API call fails)
        counter = load["loadboard_rate"]
        # Convert initial_offer to int if it's a string
        try:
            initial_offer = int(initial_offer)
        except (ValueError, TypeError):
            initial_offer = 0  # or handle as you wish
        rounds = 0
        accepted = False
        negotiation_history = []
        while rounds < max_rounds:
            negotiation_history.append({"round": rounds+1, "carrier_offer": initial_offer, "broker_offer": counter})
            if abs(initial_offer - counter) <= 100:
                accepted = True
                break
            counter = int((counter + initial_offer) / 2)
            rounds += 1
        return {"accepted": accepted, "final_rate": counter if accepted else None, "history": negotiation_history}

    def classify_outcome(self, negotiation_result):
        if negotiation_result["accepted"]:
            return "Deal Closed"
        return "No Deal"

    def classify_sentiment(self, call_transcript):
        blob = TextBlob(call_transcript)
        polarity = blob.sentiment.polarity
        if polarity > 0.2:
            return "Positive"
        elif polarity < -0.2:
            return "Negative"
        else:
            return "Neutral"

    def log_negotiation(self, data):
        try:
            requests.post(f"{API_URL}/log_negotiation", json=data, headers=HEADERS, timeout=10)
        except Exception as e:
            print(f"Failed to log negotiation: {e}")
