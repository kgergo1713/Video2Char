@echo off
REM ASCII Video Player - Gyors indító Windows-ra

echo ============================================================
echo ASCII VIDEO PLAYER - Inditas...
echo ============================================================
echo.

REM Ellenőrizzük, hogy létezik-e a venv
if not exist "venv\Scripts\python.exe" (
    echo [HIBA] Virtualis kornyezet nem talalhato!
    echo.
    echo Futtasd eloszor:
    echo   python3.13 -m venv venv
    echo   .\venv\Scripts\Activate.ps1
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM Aktiválás és futtatás
call venv\Scripts\activate.bat
python run_player.py

pause
