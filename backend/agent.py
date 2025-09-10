import requests
import os
from textblob import TextBlob

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "test-api-key")
HEADERS = {"X-API-Key": API_KEY}

class CarrierAgent:
    def __init__(self):
        self.negotiation_log = []

    def verify_mc(self, mc_number):
        resp = requests.post(f"{API_URL}/verify_mc", json={"mc_number": mc_number}, headers=HEADERS)
        return resp.json()

    def search_loads(self, equipment_type=None, origin=None, destination=None):
        params = {}
        if equipment_type:
            params["equipment_type"] = equipment_type
        if origin:
            params["origin"] = origin
        if destination:
            params["destination"] = destination
        resp = requests.get(f"{API_URL}/loads", params=params, headers=HEADERS)
        return resp.json()

    def negotiate(self, load, initial_offer, max_rounds=3):
        counter = load["loadboard_rate"]
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
        requests.post(f"{API_URL}/log_negotiation", json=data, headers=HEADERS)

# Example usage:
# agent = CarrierAgent()
# mc_status = agent.verify_mc("123456")
# if mc_status["eligible"]:
#     loads = agent.search_loads(equipment_type="Dry Van", origin="Chicago, IL")
#     chosen_load = loads[0]
#     negotiation = agent.negotiate(chosen_load, initial_offer=2100)
#     outcome = agent.classify_outcome(negotiation)
#     sentiment = agent.classify_sentiment("Thanks for your help, I appreciate it!")
#     agent.log_negotiation({"mc_number": "123456", "load_id": chosen_load["load_id"], **negotiation, "outcome": outcome, "sentiment": sentiment})
