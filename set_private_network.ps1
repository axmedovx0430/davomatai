$profile = Get-NetConnectionProfile
Write-Host "Current Network Profile:"
$profile | Select-Object Name, NetworkCategory

if ($profile.NetworkCategory -ne "Private") {
    Write-Host "Switching to Private Network..."
    Set-NetConnectionProfile -NetworkCategory Private
    Write-Host "Network is now Private. Incoming connections should be allowed."
}
else {
    Write-Host "Network is already Private."
}
