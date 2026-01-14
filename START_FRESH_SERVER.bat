@echo off
echo ========================================
echo Starting Fresh Server
echo ========================================
echo.
echo Make sure old server is stopped first!
echo Press CTRL+C in any terminal running the server.
echo.
pause

cd /d "%~dp0"
echo.
echo Current directory: %CD%
echo.
echo Starting server...
echo Dashboard will be at: http://127.0.0.1:8000/dashboard
echo.
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
