class FMCSAService:
    @staticmethod
    def verify_mc(mc_number: str):
        valid_mc = {"123456", "654321"}
        return {"mc_number": mc_number, "eligible": mc_number in valid_mc}
