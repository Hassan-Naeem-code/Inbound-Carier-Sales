FROM python:3.11-slim
WORKDIR /app
# Copy all code and data from root (no backend/)
COPY . /app
RUN pip install --no-cache-dir fastapi uvicorn streamlit textblob python-dotenv
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
