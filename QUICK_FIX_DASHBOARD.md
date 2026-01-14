# Quick Fix: Dashboard Not Showing

## Problem
Server is running but dashboard returns 404 - this means the server is running **old code**.

## Solution: Restart Server with Updated Code

### Step 1: Stop ALL Server Processes

**Option A: Use the script:**
```bash
cd Livestock-Disease
python stop_server.py
```

**Option B: Manual stop:**
- Find the terminal where server is running
- Press `CTRL + C`
- Wait for it to stop

**Option C: Kill all processes on port 8000:**
```bash
# In Command Prompt (not Git Bash):
netstat -ano | findstr :8000
# Note the PID numbers, then:
taskkill /PID <PID_NUMBER> /F
```

### Step 2: Verify Port is Free
```bash
netstat -ano | findstr :8000
```
Should show **NO LISTENING** entries.

### Step 3: Start Server Fresh
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
python -m uvicorn app.main:app --reload
```

**Wait for:**
```
INFO:     Application startup complete.
```

### Step 4: Test Dashboard
1. Open browser
2. Go to: **http://127.0.0.1:8000/dashboard**
3. Use **CTRL + F5** (hard refresh) if needed

## Alternative: Use the Restart Script

Double-click: `restart_server_fresh.bat`

This will:
1. Stop all old processes
2. Wait 3 seconds
3. Start fresh server

## Verify It's Working

After restart, test:
- http://127.0.0.1:8000/ → Should show JSON
- http://127.0.0.1:8000/docs → Should show API docs
- http://127.0.0.1:8000/dashboard → Should show HTML dashboard

If dashboard still doesn't work after fresh restart, there's a code issue. Let me know!
