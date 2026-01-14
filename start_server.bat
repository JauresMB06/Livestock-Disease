@echo off
echo ========================================
echo Livestock Disease Surveillance Network
echo Starting API Server...
echo ========================================
echo.

REM Change to the script's directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python first
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo ERROR: Cannot find app\main.py
    echo Please make sure you're in the Livestock-Disease directory
    pause
    exit /b 1
)

echo Current directory: %CD%
echo.
echo Starting server on http://127.0.0.1:8000
echo Press CTRL+C to stop the server
echo.
echo ========================================
echo.

REM Start the server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

pause
