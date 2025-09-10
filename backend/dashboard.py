import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "test-api-key")
HEADERS = {"X-API-Key": API_KEY}

st.title("Inbound Carrier Sales Dashboard")

# Metrics
st.header("Negotiation Metrics")
resp = requests.get(f"{API_URL}/metrics", headers=HEADERS)
if resp.status_code == 200:
    metrics = resp.json()
    st.metric("Total Negotiations", metrics.get("negotiations", 0))
else:
    st.error("Failed to fetch metrics.")

# Negotiation log (simple display)
try:
    with open("backend/negotiations.log") as f:
        lines = f.readlines()
    st.header("Negotiation Log")
    for line in lines[-10:]:
        st.json(line)
except FileNotFoundError:
    st.info("No negotiations logged yet.")
