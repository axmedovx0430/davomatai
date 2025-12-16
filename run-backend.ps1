# Backend ishga tushirish skripti
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Backend serverni ishga tushirish" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Backend papkasiga o'tish
Set-Location -Path "$PSScriptRoot\backend"

# Virtual environment mavjudligini tekshirish
if (-Not (Test-Path "venv")) {
    Write-Host "Virtual environment topilmadi. Yaratilmoqda..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "Virtual environment yaratildi!" -ForegroundColor Green
}

# Virtual environment aktivlashtirish
Write-Host "Virtual environment aktivlashtirilmoqda..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Kutubxonalarni o'rnatish
if (-Not (Test-Path "venv\Lib\site-packages\fastapi")) {
    Write-Host "Kerakli kutubxonalar o'rnatilmoqda..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "Kutubxonalar o'rnatildi!" -ForegroundColor Green
}

# .env faylini tekshirish
if (-Not (Test-Path ".env")) {
    Write-Host "OGOHLANTIRISH: .env fayli topilmadi!" -ForegroundColor Red
    Write-Host "Iltimos, .env faylini yarating va kerakli o'zgaruvchilarni kiriting." -ForegroundColor Red
    Write-Host ""
}

# Backend serverni ishga tushirish
Write-Host ""
Write-Host "Backend server ishga tushirilmoqda..." -ForegroundColor Green
Write-Host "Server manzili: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API hujjatlari: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "To'xtatish uchun Ctrl+C bosing" -ForegroundColor Yellow
Write-Host ""

python main.py
