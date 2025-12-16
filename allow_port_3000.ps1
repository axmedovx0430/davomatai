
New-NetFirewallRule -DisplayName "Allow Port 3000" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Allow Port 3000 Outbound" -Direction Outbound -LocalPort 3000 -Protocol TCP -Action Allow
Write-Host "Port 3000 allowed in firewall."
