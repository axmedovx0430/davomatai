# Frontend ishga tushirish skripti
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Frontend serverni ishga tushirish" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Frontend papkasiga o'tish
Set-Location -Path "$PSScriptRoot\frontend"

# node_modules mavjudligini tekshirish
if (-Not (Test-Path "node_modules")) {
    Write-Host "node_modules topilmadi. Kutubxonalar o'rnatilmoqda..." -ForegroundColor Yellow
    npm install
    Write-Host "Kutubxonalar o'rnatildi!" -ForegroundColor Green
}

# .env.local faylini tekshirish
if (-Not (Test-Path ".env.local")) {
    Write-Host "OGOHLANTIRISH: .env.local fayli topilmadi!" -ForegroundColor Yellow
    Write-Host "Agar kerak bo'lsa, .env.local faylini yarating." -ForegroundColor Yellow
    Write-Host ""
}

# Frontend serverni ishga tushirish
Write-Host ""
Write-Host "Frontend server ishga tushirilmoqda..." -ForegroundColor Green
Write-Host "Server manzili: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "To'xtatish uchun Ctrl+C bosing" -ForegroundColor Yellow
Write-Host ""

npm run dev
