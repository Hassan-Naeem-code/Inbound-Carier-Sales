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
# Health check (no auth required)
curl https://happyrobot-inbound.fly.dev/health

# Get loads (requires API key from .env)
curl -H "X-API-Key: your-api-key" https://happyrobot-inbound.fly.dev/loads

# Get specific load
curl -H "X-API-Key: your-api-key" https://happyrobot-inbound.fly.dev/load/L001
```

## 🔐 Environment Configuration

### Quick Setup
```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with your credentials
nano .env

# 3. Run setup script
./start.sh
```

### Environment Variables
All sensitive configuration is stored in environment variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `API_KEY` | API authentication key | ✅ Yes | - |
| `FMCSA_API_TOKEN` | FMCSA API authentication token | ✅ Yes | - |
| `API_URL` | Base API URL | No | `http://localhost:8000` |
| `PORT` | Server port | No | `8000` |
| `ENVIRONMENT` | Environment type | No | `development` |
| `LOG_LEVEL` | Logging level | No | `INFO` |

### Security Features
- ✅ No hardcoded credentials in source code
- ✅ Environment variables validation on startup
- ✅ `.env` file in `.gitignore` 
- ✅ `.env.example` template provided
- ✅ Centralized configuration management

## 🐳 Local Development

### Using Docker
1. Copy environment file:
   ```sh
   cp .env.example .env
   nano .env  # Edit with your credentials
   ```
2. Build the Docker image:
   ```sh
   docker build -t happyrobot-inbound .
   ```
3. Run the container:
   ```sh
   docker run -p 8000:8000 --env-file .env happyrobot-inbound
   ```

### Direct Python
1. Set up environment:
   ```sh
   ./start.sh  # Automated setup script
   ```
   Or manually:
   ```sh
   cp .env.example .env
   nano .env  # Edit with your credentials
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
3. Access the dashboard:
   ```
   http://localhost:8000/dashboard
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
fly secrets set FMCSA_API_TOKEN=your-fmcsa-token
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

### Dashboard
The dashboard is integrated into the FastAPI application and can be accessed at:
```
https://happyrobot-inbound.fly.dev/dashboard
```

## 📁 Project Structure
```
├── main.py              # FastAPI application entry point
├── agent.py             # Carrier agent logic
├── api/dashboard_view.py # Integrated dashboard
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── fly.toml            # Fly.io deployment config
├── README.md           # Project documentation
├── start.sh            # Development setup script
├── .env                # Environment variables (not in git)
├── .env.example        # Environment template
├── api/                # API route modules
│   ├── __init__.py
│   ├── loads.py        # Load search endpoints
│   ├── negotiation.py  # Negotiation logging
│   ├── webhook.py      # HappyRobot webhook
│   └── auth.py         # MC verification endpoints
├── core/               # Core utilities
│   ├── __init__.py
│   ├── config.py       # Centralized configuration
│   └── security.py     # API key validation
├── services/           # Business services
│   ├── __init__.py
│   └── fmcsa.py        # FMCSA API integration
└── data/               # Data files
    └── loads.json      # Sample load data
```

## 🛠️ Technical Features

### Performance Optimizations
- Lazy loading of JSON data to prevent startup delays
- Error handling for graceful degradation
- Optimized Docker build with layer caching
- Health checks with appropriate timeouts
- Cleaned codebase with no duplicate files

### Reliability Features
- Automatic rollback on failed deployments
- HTTP health checks every 15 seconds
- 60-second grace period for startup
- Error isolation between API modules
- Real FMCSA API integration with fallback handling

### FMCSA Integration Features
- Real-time motor carrier verification
- Comprehensive carrier eligibility checking
- Safety rating retrieval
- Graceful API failure handling
- Detailed rejection reason reporting

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

**Last Updated**: September 17, 2025  
**Deployment Status**: ✅ Live Production  
**Codebase Status**: ✅ Cleaned & Optimized
# CI/CD Pipeline Active 🚀
