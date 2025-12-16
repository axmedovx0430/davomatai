# Backend va Frontend ni bir vaqtda ishga tushirish skripti
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backend va Frontend ishga tushirish" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Backend ishga tushirish (yangi terminalda)
Write-Host "Backend serverni ishga tushirish..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run-backend.ps1"

# 3 soniya kutish
Write-Host "Backend ishga tushirildi. 3 soniya kutilmoqda..." -ForegroundColor Green
Start-Sleep -Seconds 3

# Frontend ishga tushirish (yangi terminalda)
Write-Host "Frontend serverni ishga tushirish..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\run-frontend.ps1"

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Ikkala server ham ishga tushirildi!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Serverlarni to'xtatish uchun har bir terminal oynasida Ctrl+C bosing" -ForegroundColor Yellow
