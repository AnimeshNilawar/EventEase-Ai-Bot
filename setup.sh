#!/bin/bash

# EventEase AI Bot - Quick Start Script
# This script helps you test the application locally before deploying

echo "🚀 EventEase AI Bot - Local Setup"
echo "================================="

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js are available"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd app

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
DEBUG=True
FRONTEND_ORIGIN=http://localhost:5173
DATA_DIR=data
VECTOR_DIR=data/vector_store
USE_GRADIENT=True
GRADIENT_API_BASE=https://inference.do-ai.run
GRADIENT_MODEL=gpt-4o-mini
USE_GRADIENT_EMBEDDINGS=True
GRADIENT_API_KEY=your_gradient_api_key_here
GRADIENT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EOF
    echo "⚠️  Please edit app/.env and add your Gradient AI API credentials"
fi

cd ..

# Setup frontend
echo ""
echo "🎨 Setting up frontend..."
cd eventease-frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit app/.env with your Gradient AI API credentials"
echo "2. Start the backend: cd app && source venv/bin/activate && uvicorn main:app --reload"
echo "3. Start the frontend: cd eventease-frontend && npm run dev"
echo "4. Visit http://localhost:5173 to test the application"
echo ""
echo "🚀 Ready for DigitalOcean deployment!"
echo "Follow the instructions in DEPLOYMENT.md"