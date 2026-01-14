@echo off
echo ========================================
echo Stopping old server processes...
echo ========================================
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Stopping process %%a
    taskkill /PID %%a /F >nul 2>&1
)
timeout /t 3 /nobreak >nul
echo.
echo ========================================
echo Starting fresh server...
echo ========================================
cd /d "%~dp0"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
pause
