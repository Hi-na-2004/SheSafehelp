#!/bin/bash

# SheSafe - Quick Start Script for Unix-like systems

echo "🛡️  SheSafe - Women Safety Application"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials"
fi

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting application..."
echo ""

# Start the application
cd backend
python app.py

