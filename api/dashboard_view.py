from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
import os
import json
import requests
from core.config import Config

router = APIRouter()

@router.get("/dashboard", response_class=HTMLResponse)
async def show_dashboard(request: Request):
    """
    Renders a simple dashboard directly in the FastAPI application
    This avoids the need for a separate Streamlit process
    """
    # Get metrics data from the API
    try:
        metrics_response = requests.get(
            f"{Config.API_URL}/metrics", 
            headers={"X-API-Key": Config.API_KEY},
            timeout=5
        )
        metrics = metrics_response.json() if metrics_response.status_code == 200 else {"negotiations": 0}
    except Exception as e:
        metrics = {"negotiations": 0, "error": str(e)}
    
    # Try to read negotiation logs
    logs = []
    try:
        log_path = os.path.join(os.path.dirname(__file__), '../data/negotiations.log')
        if os.path.exists(log_path):
            with open(log_path) as f:
                lines = f.readlines()
                # Get the last 10 logs
                for line in lines[-10:]:
                    try:
                        logs.append(json.loads(line))
                    except:
                        logs.append({"error": "Failed to parse log entry", "raw": line.strip()})
    except Exception as e:
        logs = [{"error": str(e)}]
    
    # HTML template for the dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inbound Carrier Sales Dashboard</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            h1, h2 {{
                color: #2C3E50;
            }}
            .metric-card {{
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .metric-value {{
                font-size: 2.5rem;
                font-weight: bold;
                color: #3498DB;
                margin: 10px 0;
            }}
            .metric-label {{
                font-size: 1rem;
                color: #7f8c8d;
            }}
            .log-entry {{
                background-color: #f8f9fa;
                border-left: 4px solid #3498DB;
                padding: 15px;
                margin: 10px 0;
                border-radius: 4px;
                overflow-x: auto;
            }}
            .log-entry pre {{
                margin: 0;
                white-space: pre-wrap;
            }}
            .container {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                justify-content: space-between;
            }}
            .container > div {{
                flex: 1;
                min-width: 300px;
            }}
            .auto-refresh {{
                color: #7f8c8d;
                font-size: 0.9rem;
                text-align: center;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <h1>Inbound Carrier Sales Dashboard</h1>
        
        <div class="container">
            <div>
                <h2>Negotiation Metrics</h2>
                <div class="metric-card">
                    <div class="metric-label">Total Negotiations</div>
                    <div class="metric-value">{metrics.get("negotiations", 0)}</div>
                </div>
            </div>
            
            <div>
                <h2>Recent Activity</h2>
                <div class="metric-card">
                    <div class="metric-label">Recent Negotiations</div>
                    <div class="metric-value">{len(logs)}</div>
                </div>
            </div>
        </div>
        
        <h2>Negotiation Logs</h2>
    """
    
    # Add logs to HTML
    if logs:
        for log in logs:
            html_content += f"""
            <div class="log-entry">
                <pre>{json.dumps(log, indent=2)}</pre>
            </div>
            """
    else:
        html_content += '<div class="log-entry"><pre>No negotiations logged yet.</pre></div>'
    
    # Auto-refresh script and close HTML tags
    html_content += """
        <div class="auto-refresh">Dashboard auto-refreshes every 30 seconds</div>
        
        <script>
            // Auto-refresh the page every 30 seconds
            setTimeout(function() {
                location.reload();
            }, 30000);
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)