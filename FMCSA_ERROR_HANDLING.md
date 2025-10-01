# FMCSA API Error Handling Guide

## Common FMCSA API Errors and Solutions

### Error: HTTP 500 - Internal Server Error
```json
{
  "content": "We encountered an error while processing your request. Please try a different request or try again later. Error ID: C645C811",
  "retrievalDate": "2025-10-01T21:57:57.736+0000"
}
```

**Causes:**
1. FMCSA API server overload
2. Invalid API token
3. Rate limiting
4. Maintenance windows

**Solutions Implemented:**
1. **Retry Logic**: Up to 3 attempts with exponential backoff
2. **Intelligent Fallback**: Format validation when API fails
3. **Caching**: 5-minute cache to reduce API calls
4. **Better Error Handling**: Detailed logging and graceful degradation

### Error Handling Flow

1. **Format Validation** → Check MC number is numeric
2. **Cache Check** → Return cached result if available
3. **API Call with Retry** → Up to 3 attempts
4. **Intelligent Fallback** → If API fails, validate format and allow with warning
5. **Cache Result** → Store for future requests

### Deployment Recommendations

#### Environment Variables
```bash
# Fly.io secrets
fly secrets set FMCSA_API_TOKEN=your-actual-token
fly secrets set API_KEY=your-secure-api-key
fly secrets set LOG_LEVEL=INFO
```

#### Monitoring Endpoints
- `GET /fmcsa/health` - Check FMCSA API status
- `GET /fmcsa/cache/stats` - View cache statistics
- `POST /fmcsa/cache/clear` - Clear cache if needed

### Testing the Fixes

#### Local Testing
```bash
# Test with known working MC
curl -X POST "http://localhost:8000/verify_mc" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"mc_number": 123456}'

# Check FMCSA health
curl "http://localhost:8000/fmcsa/health" \
  -H "X-API-Key: your-api-key"
```

#### HappyRobot Integration
The API now handles FMCSA failures gracefully:
- Valid MC numbers will still return `eligible: true` during API outages
- Invalid format MC numbers will return `eligible: false`
- All responses include detailed status information

### Response Format Changes

#### Success Response (unchanged)
```json
{
  "eligible": true,
  "mc_number": "123456",
  "status": "verified",
  "legal_name": "CARRIER NAME"
}
```

#### Fallback Response (new)
```json
{
  "eligible": true,
  "mc_number": "123456", 
  "status": "api_server_error",
  "message": "FMCSA API temporarily unavailable (FMCSA API server error). MC format appears valid.",
  "legal_name": "Unknown (API Error)",
  "fallback_reason": "FMCSA API server error"
}
```

### Production Deployment

1. **Deploy with fixes**:
   ```bash
   fly deploy
   ```

2. **Monitor logs**:
   ```bash
   fly logs
   ```

3. **Test health**:
   ```bash
   curl https://happyrobot-inbound.fly.dev/fmcsa/health -H "X-API-Key: your-key"
   ```

The system now gracefully handles FMCSA API failures while maintaining compatibility with your HappyRobot workflow!