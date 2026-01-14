@echo off
echo Stopping any existing Python servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting FastAPI server...
cd /d "%~dp0"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
