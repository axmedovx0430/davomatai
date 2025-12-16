@echo off
echo Opening Port 8000 in Windows Firewall...
netsh advfirewall firewall delete rule name="DavomatAI Backend"
netsh advfirewall firewall add rule name="DavomatAI Backend" dir=in action=allow protocol=TCP localport=8000 profile=any
echo Done!
pause
