# HappyRobot Inbound Carrier Sales API

## 🚀 Live Deployment
**Production URL**: https://happyrobot-inbound.fly.dev/

## Overview
This API powers the inbound carrier sales automation for Acme Logistics using the HappyRobot platform. It provides endpoints for load search, MC number verification, negotiation logging, metrics reporting, and a webhook for HappyRobot integration.

The application is deployed on Fly.io with automated health checks and optimized for fast startup.

## 📋 API Endpoints

### Core Endpoints
- `GET /` — API status and information
- `GET /health` — Health check endpoint (for monitoring)
- `GET /loads` — Search available loads (filter by equipment, origin, destination)
- `GET /load/{load_id}` — Get details for a specific load
- `POST /verify_mc` — Verify carrier MC number (FMCSA integration)
- `POST /log_negotiation` — Log negotiation data
- `GET /metrics` — Get negotiation/call metrics
- `POST /webhook/happyrobot` — Webhook for HappyRobot web call trigger

### Example API Usage
```bash
# Health check
curl https://happyrobot-inbound.fly.dev/health

# Get loads (requires API key)
curl -H "X-API-Key: your-api-key" https://happyrobot-inbound.fly.dev/loads

# Get specific load
curl -H "X-API-Key: your-api-key" https://happyrobot-inbound.fly.dev/load/L001
```

## 🔐 Security
- All endpoints require an API key via the `X-API-Key` header (except `/webhook/happyrobot` and health endpoints)
- Default API key: `test-api-key` (change via `API_KEY` environment variable)
- HTTPS enabled by default on Fly.io deployment

## 🐳 Local Development

### Using Docker
1. Build the Docker image:
   ```sh
   docker build -t happyrobot-inbound .
   ```
2. Run the container:
   ```sh
   docker run -p 8000:8000 -e API_KEY=test-api-key happyrobot-inbound
   ```
3. Access the API at `http://localhost:8000`

### Direct Python
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. Run the dashboard:
   ```sh
   streamlit run dashboard.py
   ```

## ☁️ Production Deployment (Fly.io)

### Current Configuration
- **App Name**: `happyrobot-inbound`
- **Region**: `ord` (Chicago)
- **Memory**: 1GB
- **CPU**: 1 shared CPU
- **Health Checks**: Automated HTTP checks on `/health`

### Deployment Commands
```sh
# Deploy to Fly.io
fly deploy

# Check status
fly status

# View logs
fly logs

# Scale app
fly scale count 2
```

### Environment Variables
Set via Fly.io secrets:
```sh
fly secrets set API_KEY=your-secure-api-key
```

## 🔗 HappyRobot Integration

Configure the HappyRobot platform to POST call data to the webhook endpoint:

**Webhook URL**: `https://happyrobot-inbound.fly.dev/webhook/happyrobot`

**Example Payload**:
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

## 📊 Monitoring & Dashboard

### Health Monitoring
- **Health Check**: https://happyrobot-inbound.fly.dev/health
- **Status Page**: Available through Fly.io dashboard
- **Logs**: `fly logs --app happyrobot-inbound`

### Local Dashboard
Run the Streamlit dashboard for metrics visualization:
```sh
streamlit run dashboard.py
```

## 📁 Project Structure
```
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── fly.toml            # Fly.io deployment config
├── dashboard.py        # Streamlit dashboard
├── api/                # API route modules
│   ├── loads.py        # Load search endpoints
│   ├── negotiation.py  # Negotiation logging
│   ├── webhook.py      # HappyRobot webhook
│   └── auth.py         # Authentication endpoints
├── core/               # Core utilities
│   ├── config.py       # Configuration management
│   └── security.py     # API key validation
├── data/               # Data files
│   └── loads.json      # Sample load data
└── models/             # Data models
    ├── load.py         # Load data structures
    ├── mc.py           # MC verification models
    └── negotiation.py  # Negotiation models
```

## 🛠️ Technical Features

### Performance Optimizations
- Lazy loading of JSON data to prevent startup delays
- Error handling for graceful degradation
- Optimized Docker build with layer caching
- Health checks with appropriate timeouts

### Reliability Features
- Automatic rollback on failed deployments
- HTTP health checks every 15 seconds
- 60-second grace period for startup
- Error isolation between API modules

## 🚀 Scaling & Maintenance

### Scaling Up
```sh
# Increase instance count
fly scale count 3

# Upgrade memory
fly scale memory 2048

# Add more CPU
fly scale vm performance-2x
```

### Updates
```sh
# Deploy new version
git push origin main
fly deploy

# Rollback if needed
fly releases list
fly releases rollback <version>
```

## 📞 Support

For technical support or questions:
- Check application logs: `fly logs`
- Monitor health: https://happyrobot-inbound.fly.dev/health
- Review Fly.io dashboard for performance metrics

---

**Last Updated**: September 15, 2025  
**Deployment Status**: ✅ Live Production
