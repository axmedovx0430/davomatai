# ESP32-CAM Davomat Tizimi - Quick Start Script (Windows)

Write-Host "🚀 ESP32-CAM Davomat Tizimi - Quick Start" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python topilmadi. Iltimos Python 3.8+ o'rnating." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  Node.js topilmadi. Iltimos Node.js 18+ o'rnating." -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 1. Backend sozlash..." -ForegroundColor Cyan
Set-Location backend

# Create virtual environment
if (-not (Test-Path "venv")) {
    Write-Host "   Virtual environment yaratilmoqda..." -ForegroundColor Gray
    python -m venv venv
}

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "   Dependencies o'rnatilmoqda..." -ForegroundColor Gray
pip install -q -r requirements.txt

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "   .env fayl yaratilmoqda..." -ForegroundColor Gray
    Copy-Item .env.example .env
    Write-Host "   ⚠️  .env faylni tahrirlang va to'ldiring!" -ForegroundColor Yellow
}

Set-Location ..

Write-Host ""
Write-Host "📦 2. Frontend sozlash..." -ForegroundColor Cyan
Set-Location frontend

# Install dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "   Dependencies o'rnatilmoqda..." -ForegroundColor Gray
    npm install
}

# Create .env.local if not exists
if (-not (Test-Path ".env.local")) {
    Write-Host "   .env.local yaratilmoqda..." -ForegroundColor Gray
    "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath .env.local -Encoding utf8
}

Set-Location ..

Write-Host ""
Write-Host "✅ Sozlash tugadi!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Keyingi qadamlar:" -ForegroundColor Cyan
Write-Host "   1. PostgreSQL database yarating (pgAdmin yoki psql orqali)"
Write-Host "      CREATE DATABASE attendance_db;"
Write-Host "      Keyin backend/database/schema.sql ni import qiling"
Write-Host ""
Write-Host "   2. backend/.env faylni to'ldiring"
Write-Host ""
Write-Host "   3. Backend ishga tushiring:"
Write-Host "      cd backend"
Write-Host "      .\venv\Scripts\Activate.ps1"
Write-Host "      python main.py"
Write-Host ""
Write-Host "   4. Frontend ishga tushiring (yangi terminal):"
Write-Host "      cd frontend"
Write-Host "      npm run dev"
Write-Host ""
Write-Host "   5. Brauzerda oching: http://localhost:3000"
Write-Host ""
