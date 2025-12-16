New-NetFirewallRule -DisplayName "DavomatAI Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
Write-Host "Port 8000 opened successfully!"
