@echo off
echo Opening Port 8080 in Windows Firewall...
netsh advfirewall firewall delete rule name="DavomatAI Backend 8080"
netsh advfirewall firewall add rule name="DavomatAI Backend 8080" dir=in action=allow protocol=TCP localport=8080 profile=any
echo Done!
pause
