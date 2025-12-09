# ASCII Video Player - Gyors indító PowerShell script

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ASCII VIDEO PLAYER - Indítás..." -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Ellenőrizzük, hogy létezik-e a venv
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "[HIBA] Virtuális környezet nem található!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Futtasd először:" -ForegroundColor Yellow
    Write-Host "  python3.13 -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    Write-Host ""
    Read-Host "Nyomj Enter-t a kilépéshez"
    exit 1
}

# Aktiválás
& .\venv\Scripts\Activate.ps1

# Program futtatása
python run_player.py

# Ha be van zárva az ablak, várunk
if ($?) {
    Write-Host ""
    Write-Host "Program befejezve." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Hiba történt a futtatás során." -ForegroundColor Red
    Read-Host "Nyomj Enter-t a kilépéshez"
}
