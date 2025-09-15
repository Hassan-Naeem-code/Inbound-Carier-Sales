class NegotiationService:
    @staticmethod
    def negotiate(load, initial_offer, max_rounds=3):
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

    @staticmethod
    def classify_outcome(negotiation_result):
        if negotiation_result["accepted"]:
            return "Deal Closed"
        return "No Deal"
