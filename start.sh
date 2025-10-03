#!/bin/bash

# HappyRobot Inbound Carrier API Startup Script
# This script helps with local development setup

echo "🚀 HappyRobot Inbound Carrier API Setup"
echo "======================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "📋 Copying .env.example to .env..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "🔧 Please edit .env file with your actual credentials:"
    echo "   - Set your API_KEY"
    echo "   - Set your FMCSA_API_TOKEN"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Validate environment variables
echo "🔍 Validating environment configuration..."
python3 -c "from core.config import Config; print('✅ Configuration validated successfully')" || {
    echo "❌ Configuration validation failed!"
    echo "Please check your .env file and ensure all required variables are set."
    exit 1
}

echo ""
echo "🎉 Setup complete! You can now run:"
echo "   📖 API Documentation: uvicorn main:app --reload"
echo "   📊 Dashboard: http://localhost:8000/dashboard (once API is running)"
echo "   🐳 Docker: docker build -t happyrobot-local ."

# Ask if user wants to start the API
read -p "🚀 Start the API server now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌟 Starting HappyRobot API..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
fi