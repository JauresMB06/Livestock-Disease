# Step-by-Step Guide: How to Run the Server

## Prerequisites
Make sure you have Python installed. Check by running:
```bash
python --version
```

## Step 1: Open Terminal/Command Prompt

**Option A: Using Command Prompt**
- Press `Windows Key + R`
- Type `cmd` and press Enter

**Option B: Using PowerShell**
- Press `Windows Key + X`
- Select "Windows PowerShell" or "Terminal"

**Option C: Using Git Bash** (if you have Git installed)
- Right-click in the folder → "Git Bash Here"

## Step 2: Navigate to the Project Directory

Type these commands one by one (press Enter after each):

```bash
cd Desktop
cd Livestock-Disease
```

**OR** if you're already on Desktop:
```bash
cd Livestock-Disease
```

**OR** use the full path:
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
```

## Step 3: Verify You're in the Right Directory

Check that you can see the project files:
```bash
dir
```

You should see files like:
- `app` (folder)
- `requirements.txt`
- `run_demo.py`
- etc.

## Step 4: Check if Dependencies are Installed

First, verify FastAPI is installed:
```bash
python -c "import fastapi; print('FastAPI installed!')"
```

If you get an error, install dependencies:
```bash
pip install fastapi uvicorn
```

## Step 5: Start the Server

Run this command:
```bash
uvicorn app.main:app --reload
```

**What you should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 6: Test the Server

**Keep the terminal running!** Open a NEW terminal/browser and:

1. **Test in Browser:**
   - Open: http://127.0.0.1:8000
   - Should see: `{"message":"LDSN API is running"}`

2. **Test Interactive Docs:**
   - Open: http://127.0.0.1:8000/docs
   - You'll see the Swagger UI with all API endpoints

## Common Issues and Solutions

### Issue 1: "uvicorn is not recognized"
**Solution:**
```bash
pip install uvicorn
```

### Issue 2: "No module named 'fastapi'"
**Solution:**
```bash
pip install fastapi uvicorn
```

### Issue 3: "No module named 'app'"
**Solution:** Make sure you're in the `Livestock-Disease` directory:
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
dir  # Should see 'app' folder
```

### Issue 4: Port 8000 already in use
**Solution:** Use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue 5: Command doesn't work in Git Bash
**Solution:** Use Command Prompt or PowerShell instead, or use:
```bash
python -m uvicorn app.main:app --reload
```

## Alternative: Using Python Module Syntax

If `uvicorn` command doesn't work, try:
```bash
python -m uvicorn app.main:app --reload
```

## To Stop the Server

Press `CTRL + C` in the terminal where the server is running.

## Quick Reference

**Full command sequence:**
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
uvicorn app.main:app --reload
```

**Or using Python module:**
```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
python -m uvicorn app.main:app --reload
```
