# Check and Stop Server

## ✅ Server Status Check

The server was running on port 8000 (PID 13676). 

## How to Stop the Server Manually:

### Method 1: Using the Script (Easiest)
```bash
cd Livestock-Disease
python stop_server.py
```

### Method 2: Manual Stop
1. **Find the terminal** where the server is running
2. **Press `CTRL + C`** to stop it
3. **Wait** for it to fully stop

### Method 3: Kill Process (if stuck)
Open Command Prompt (not Git Bash) and run:
```cmd
taskkill /PID 13676 /F
```

Or find and kill all Python processes:
```cmd
tasklist | findstr python
taskkill /IM python.exe /F
```
⚠️ **Warning:** This will kill ALL Python processes!

## Verify Server is Stopped:

```bash
netstat -ano | findstr :8000
```

If you see **no output**, the port is free!

## After Stopping:

Start the server fresh:
```bash
cd Livestock-Disease
uvicorn app.main:app --reload
```

Then access: http://127.0.0.1:8000/dashboard
