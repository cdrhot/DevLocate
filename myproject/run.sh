#!/bin/bash
# Quick Start Guide for DevLocate

echo "================================"
echo "DevLocate - Nearby Users Edition"
echo "================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found"
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
    echo ""
    echo "🚀 Starting FastAPI server..."
    echo ""
    echo "Application will be available at: http://localhost:8000"
    echo ""
    echo "Available endpoints:"
    echo "  - http://localhost:8000                    (Main app)"
    echo "  - http://localhost:8000/docs               (API Docs)"
    echo "  - http://localhost:8000/redoc              (ReDoc)"
    echo ""
    echo "API Endpoints:"
    echo "  - GET /api/osm/route                       (Find routes)"
    echo "  - GET /api/users/nearby                    (Find nearby users)"
    echo "  - GET /api/users/all                       (Get all users)"
    echo "  - GET /health                              (Health check)"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
