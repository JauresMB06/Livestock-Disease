# Dashboard Troubleshooting Guide

## ✅ Route is Correctly Registered

The `/dashboard` route is properly defined and working. If you're getting a 404 error, try these solutions:

## Solution 1: Clear Browser Cache

1. **Hard Refresh:**
   - Windows/Linux: `CTRL + F5` or `CTRL + SHIFT + R`
   - Mac: `CMD + SHIFT + R`

2. **Or clear cache:**
   - Open browser settings
   - Clear browsing data/cache
   - Try accessing again

## Solution 2: Verify Server is Running Latest Code

1. **Stop the server completely:**
   ```bash
   # Press CTRL+C in the terminal
   ```

2. **Verify you're in the right directory:**
   ```bash
   cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
   dir app\main.py
   ```

3. **Start server with explicit reload:**
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

4. **Check the startup messages:**
   - Should see: "Application startup complete"
   - Should NOT see any import errors

## Solution 3: Test the Route Directly

**Option A: Using curl (if available):**
```bash
curl http://127.0.0.1:8000/dashboard
```

**Option B: Using Python:**
```bash
python -c "import requests; r = requests.get('http://127.0.0.1:8000/dashboard'); print('Status:', r.status_code); print('Content length:', len(r.text))"
```

**Option C: Check in browser:**
- Open: http://127.0.0.1:8000/docs
- Look for `/dashboard` in the list of endpoints
- Click "Try it out" to test

## Solution 4: Check for Port Conflicts

Make sure nothing else is using port 8000:

```bash
# Windows
netstat -ano | findstr :8000

# If something is using it, kill it or use a different port
```

## Solution 5: Verify URL

Make sure you're accessing:
- ✅ **Correct:** http://127.0.0.1:8000/dashboard
- ✅ **Correct:** http://localhost:8000/dashboard
- ❌ **Wrong:** http://127.0.0.1:8000/api/dashboard
- ❌ **Wrong:** http://127.0.0.1:8000/dashboard/

## Solution 6: Check Server Logs

When you start the server, you should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

If you see errors, that's the problem!

## Solution 7: Test with Simple Route First

Add this to `app/main.py` to test:

```python
@app.get("/test")
def test():
    return {"message": "Server is working"}
```

Then access: http://127.0.0.1:8000/test

If this works but `/dashboard` doesn't, there's a specific issue with the dashboard route.

## Quick Fix Command Sequence

```bash
# 1. Stop server (CTRL+C)

# 2. Navigate to project
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease

# 3. Verify file exists
dir app\main.py

# 4. Start server
python -m uvicorn app.main:app --reload

# 5. In browser, try:
# http://127.0.0.1:8000/dashboard
# (Use CTRL+F5 to hard refresh)
```

## Still Not Working?

If none of these work, the issue might be:
1. **Python environment:** Make sure you're using the same Python that has FastAPI installed
2. **File encoding:** The HTML might have encoding issues
3. **FastAPI version:** Try updating: `pip install --upgrade fastapi uvicorn`

Let me know what error message you see in the browser or server logs!
