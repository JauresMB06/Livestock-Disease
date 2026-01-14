@echo off
echo Stopping server on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /PID %%a /F
)
timeout /t 2 /nobreak >nul
netstat -ano | findstr :8000
if errorlevel 1 (
    echo Server stopped successfully!
) else (
    echo Server may still be running. Check manually.
)
pause
