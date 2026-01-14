# How to Restart the Server

## Quick Steps

1. **Stop the server:**
   - Find the terminal/command prompt where the server is running
   - Press `CTRL + C`
   - Wait 2-3 seconds

2. **Start the server:**
   ```bash
   cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
   python -m uvicorn app.main:app --reload
   ```

3. **Wait for startup:**
   - You should see: `INFO: Application startup complete.`
   - Server URL: http://127.0.0.1:8000

4. **Test the dashboard:**
   - Open: http://127.0.0.1:8000/dashboard
   - Press `CTRL + F5` to hard refresh
   - Click the Quick Link buttons

## Alternative: Use Batch Script

Double-click: `restart_server_now.bat`

## Verify It's Working

After restart, the dashboard should:
- ✅ Have buttons (not just links) for Quick Links
- ✅ Display data when you click buttons
- ✅ Show formatted tables/cards instead of "Not Found"

---

**The code is correct - just needs a fresh server restart!**
