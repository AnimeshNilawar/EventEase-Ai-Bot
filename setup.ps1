# EventEase AI Bot - Quick Start Script (Windows PowerShell)
# This script helps you test the application locally before deploying

Write-Host "🚀 EventEase AI Bot - Local Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python is available: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8+ first." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js is available: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 16+ first." -ForegroundColor Red
    exit 1
}

# Setup backend
Write-Host ""
Write-Host "📦 Setting up backend..." -ForegroundColor Cyan
Set-Location app

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating Python virtual environment..."
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..."
    @"
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
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "⚠️  Please edit app\.env and add your Gradient AI API credentials" -ForegroundColor Yellow
}

Set-Location ..

# Setup frontend
Write-Host ""
Write-Host "🎨 Setting up frontend..." -ForegroundColor Cyan
Set-Location eventease-frontend

# Install Node.js dependencies
Write-Host "Installing Node.js dependencies..."
npm install

Set-Location ..

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit app\.env with your Gradient AI API credentials"
Write-Host "2. Start the backend:"
Write-Host "   cd app"
Write-Host "   .\venv\Scripts\Activate.ps1"
Write-Host "   uvicorn main:app --reload"
Write-Host "3. Start the frontend (in a new terminal):"
Write-Host "   cd eventease-frontend"
Write-Host "   npm run dev"
Write-Host "4. Visit http://localhost:5173 to test the application"
Write-Host ""
Write-Host "🚀 Ready for DigitalOcean deployment!" -ForegroundColor Green
Write-Host "Follow the instructions in DEPLOYMENT.md"