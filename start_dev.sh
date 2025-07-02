#!/bin/bash

# FastAPI Jumpstart Development Server
# This script starts the FastAPI development server with hot reload

echo "🚀 Starting FastAPI Jumpstart Development Server..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc Documentation: http://localhost:8000/redoc"
echo ""
echo "Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    echo "✅ Virtual environment created."
fi

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    # Windows
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    # Unix/macOS
    source venv/bin/activate
fi

# Install dependencies if requirements.txt is newer than the last install
if [ ! -f ".last_install" ] || [ "requirements.txt" -nt ".last_install" ]; then
    echo "📦 Installing/updating dependencies..."
    pip install -r requirements.txt
    touch .last_install
    echo "✅ Dependencies installed."
fi

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
