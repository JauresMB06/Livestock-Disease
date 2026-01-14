# Start Server - Quick Guide

## ✅ Server is Starting!

The server is being started in the background. Here's what to do:

## Step 1: Wait for Server to Start

Wait about 5-10 seconds for the server to fully start.

## Step 2: Check if Server is Running

Open a browser and go to:
- **http://127.0.0.1:8000/**

You should see:
```json
{"message":"LDSN API is running","docs":"/docs","dashboard":"/dashboard"}
```

## Step 3: Access Dashboard

Once the server is running, go to:
- **http://127.0.0.1:8000/dashboard**

You should see the HTML dashboard page!

## Step 4: Alternative - Start Manually

If the background start didn't work, open a **NEW terminal** and run:

```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
python -m uvicorn app.main:app --reload
```

**Wait for:**
```
INFO:     Application startup complete.
```

Then access: http://127.0.0.1:8000/dashboard

## What You Should See

When the dashboard loads, you should see:
- Green header: "🐄 Livestock Disease Surveillance Network"
- Quick Links section
- Range Query (Segment Tree) section
- Summary Statistics section

## If Dashboard Still Doesn't Work

1. Check server logs for errors
2. Make sure you're using: http://127.0.0.1:8000/dashboard (no trailing slash)
3. Try hard refresh: CTRL + F5
4. Try incognito/private browser mode

---

**The server should be starting now. Give it a few seconds, then try the dashboard!**
