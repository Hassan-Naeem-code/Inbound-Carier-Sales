# HappyRobot Inbound Carrier Sales API

## Overview
This API powers the inbound carrier sales automation for Acme Logistics using the HappyRobot platform. It provides endpoints for load search, MC number verification, negotiation logging, metrics reporting, and a webhook for HappyRobot integration.

## Endpoints
- `/loads` — Search available loads (filter by equipment, origin, destination)
- `/load/{load_id}` — Get details for a specific load
- `/verify_mc` — Verify carrier MC number (FMCSA integration placeholder)
- `/log_negotiation` — Log negotiation data
- `/metrics` — Get negotiation/call metrics
- `/webhook/happyrobot` — Webhook for HappyRobot web call trigger (POST call data to automate agent logic)

## Security
- All endpoints require an API key via the `X-API-Key` header (except `/webhook/happyrobot`).
- HTTPS is recommended for deployment (self-signed for local, Let’s Encrypt for production).

## Running Locally (with Docker)
1. Build the Docker image:
   ```sh
   docker build -t happyrobot-inbound .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 -e API_KEY=test-api-key happyrobot-inbound
   ```
3. Access the API at `http://localhost:8000` (use `X-API-Key: test-api-key` in requests).
4. Run the dashboard:
   ```sh
   streamlit run dashboard.py
   ```

## HTTPS Setup (Local)
To run with HTTPS locally (self-signed):
1. Generate a self-signed certificate:
   ```sh
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
   ```
2. Run Uvicorn with SSL:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem
   ```

## Deploying to Cloud (e.g., Fly.io, Railway, AWS)
1. Push your code to a GitHub repository.
2. Follow your provider’s instructions to deploy a Docker container.
3. For HTTPS in production, use Let’s Encrypt or your provider’s SSL solution.
4. Set the `API_KEY` environment variable securely.

## HappyRobot Integration
- Configure the HappyRobot platform to POST call data to `/webhook/happyrobot`.
- Example payload:
  ```json
  {
    "mc_number": "123456",
    "equipment_type": "Dry Van",
    "origin": "Chicago, IL",
    "destination": "Dallas, TX",
    "initial_offer": 2100,
    "call_transcript": "Thanks for your help, I appreciate it!"
  }
  ```

## Dashboard
- Run with: `streamlit run dashboard.py`
- Shows negotiation metrics and recent logs.

## Reproducing Deployment
- All dependencies are in `requirements.txt` and the Dockerfile.
- For cloud, use the Dockerfile and set environment variables as needed.

---
For questions or support, contact your technical team.
