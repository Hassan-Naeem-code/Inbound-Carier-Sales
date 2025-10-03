FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks and supervisor for process management
RUN apt-get update && apt-get install -y curl supervisor && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code and data
COPY . /app

# Configure supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000 8501

# Add health check for the API
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start supervisor which will start both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]