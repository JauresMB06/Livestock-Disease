# Manual API Testing Instructions

## Step 1: Start the Server

Open a terminal/command prompt and run:

```bash
cd Livestock-Disease
uvicorn app.main:app --reload
```

Or on Windows, double-click `start_server.bat`

The server will start at: **http://127.0.0.1:8000**

## Step 2: Test the API Endpoints

### Option A: Use the Interactive Documentation

Open your browser and go to:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

You can test all endpoints directly from the browser!

### Option B: Use curl or Python

**1. Root Endpoint:**
```bash
curl http://127.0.0.1:8000/
```

**2. Get All GPS Hubs:**
```bash
curl http://127.0.0.1:8000/api/gps/hubs
```

**3. Get Specific Hub:**
```bash
curl http://127.0.0.1:8000/api/gps/hubs/Ngaoundéré
```

**4. Search Clinical Signs:**
```bash
curl "http://127.0.0.1:8000/api/clinical-signs/search?prefix=fever"
```

**5. Get Diseases for a Sign:**
```bash
curl "http://127.0.0.1:8000/api/clinical-signs/diseases?sign=fever"
```

**6. Submit a Disease Report:**
```bash
curl -X POST http://127.0.0.1:8000/api/report ^
  -H "Content-Type: application/json" ^
  -d "{\"animal_id\": \"COW001\", \"location\": \"Ngaoundéré\", \"symptoms\": \"High fever\", \"severity\": 3, \"clinical_signs\": [\"fever\"]}"
```

### Option C: Run the Test Script

In a **new terminal** (keep the server running), run:

```bash
cd Livestock-Disease
python test_api.py
```

## Summary

✅ **Demo Script**: Already completed - showed GPS coordinates and clinical signs Trie working
✅ **API Server**: Ready to start with `uvicorn app.main:app --reload`
✅ **API Endpoints**: All integrated and ready to test

The integration is complete! All your GPS coordinates and clinical signs code is now integrated with the FastAPI backend.
