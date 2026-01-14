# What to Do Next - Testing Your API

## ✅ Server is Running!

Your server is now running at: **http://127.0.0.1:8000**

## Step 1: Test the Basic Endpoint

Open your web browser and go to:
```
http://127.0.0.1:8000
```

You should see:
```json
{"message":"LDSN API is running"}
```

## Step 2: Explore Interactive API Documentation

This is the BEST way to test all endpoints! Open:
```
http://127.0.0.1:8000/docs
```

You'll see a Swagger UI interface where you can:
- See all available endpoints
- Test each endpoint directly
- See request/response examples
- Try out the API without writing code

## Step 3: Test GPS Coordinates Endpoints

### Get All Cattle Hubs:
```
http://127.0.0.1:8000/api/gps/hubs
```

### Get Specific Hub (Ngaoundéré):
```
http://127.0.0.1:8000/api/gps/hubs/Ngaoundéré
```

### Get Other Hubs:
```
http://127.0.0.1:8000/api/gps/hubs/Maroua
http://127.0.0.1:8000/api/gps/hubs/Bamenda
```

## Step 4: Test Clinical Signs Endpoints

### Get All Clinical Signs:
```
http://127.0.0.1:8000/api/clinical-signs
```

### Search Clinical Signs (Trie Search):
```
http://127.0.0.1:8000/api/clinical-signs/search?prefix=fever
http://127.0.0.1:8000/api/clinical-signs/search?prefix=lameness
http://127.0.0.1:8000/api/clinical-signs/search?prefix=swelling
```

### Get Diseases for a Clinical Sign:
```
http://127.0.0.1:8000/api/clinical-signs/diseases?sign=fever
http://127.0.0.1:8000/api/clinical-signs/diseases?sign=lameness
```

### Get Complete Dictionary:
```
http://127.0.0.1:8000/api/clinical-signs/dictionary
```

## Step 5: Test Disease Report Submission

### Using the Interactive Docs (Recommended):
1. Go to: http://127.0.0.1:8000/docs
2. Find the `POST /api/report` endpoint
3. Click "Try it out"
4. Use this example JSON:
```json
{
  "animal_id": "COW001",
  "location": "Ngaoundéré",
  "symptoms": "High fever, nasal discharge",
  "severity": 3,
  "clinical_signs": ["fever", "nasal discharge"]
}
```
5. Click "Execute"
6. See the response with GPS coordinates and associated diseases!

### Using curl (if you have it):
```bash
curl -X POST http://127.0.0.1:8000/api/report ^
  -H "Content-Type: application/json" ^
  -d "{\"animal_id\": \"COW001\", \"location\": \"Ngaoundéré\", \"symptoms\": \"High fever\", \"severity\": 3, \"clinical_signs\": [\"fever\"]}"
```

## Step 6: Run the Test Script

Open a **NEW terminal** (keep the server running in the first one) and run:

```bash
cd C:\Users\GENERAL-STORES\Desktop\Livestock-Disease
python test_api.py
```

This will test all endpoints automatically!

## What You Should See

### GPS Hubs Response:
```json
{
  "hubs": {
    "Ngaoundéré": {
      "latitude": 7.3277,
      "longitude": 13.5847,
      "city": "Ngaoundéré",
      "region": "Adamawa",
      "country": "Cameroon"
    },
    ...
  }
}
```

### Clinical Signs Search Response:
```json
{
  "prefix": "fever",
  "results": [
    {
      "clinical_sign": "fever",
      "diseases": ["Bovine Malignant Catarrhal Fever (MCF)", "Bluetongue Disease", ...]
    }
  ],
  "count": 1
}
```

### Disease Report Response:
```json
{
  "status": "received",
  "data": {
    "animal_id": "COW001",
    "location": "Ngaoundéré",
    "symptoms": "High fever",
    "severity": 3,
    "clinical_signs": ["fever"]
  },
  "associated_diseases": ["Bovine Malignant Catarrhal Fever (MCF)", ...],
  "gps_coordinates": {
    "latitude": 7.3277,
    "longitude": 13.5847
  }
}
```

## Summary of Available Endpoints

1. **GET /** - Root endpoint
2. **GET /api/gps/hubs** - Get all cattle hub coordinates
3. **GET /api/gps/hubs/{city}** - Get specific hub coordinates
4. **GET /api/clinical-signs** - Get all clinical signs
5. **GET /api/clinical-signs/search?prefix={prefix}** - Search clinical signs
6. **GET /api/clinical-signs/diseases?sign={sign}** - Get diseases for a sign
7. **GET /api/clinical-signs/dictionary** - Get complete dictionary
8. **POST /api/report** - Submit disease report (with GPS auto-detection)

## Next Steps for Development

1. ✅ **Server Running** - Done!
2. ✅ **Test Endpoints** - Do this now!
3. **Integrate with Mobile App** - Connect React Native app to this API
4. **Add Database Storage** - Store reports in database
5. **Add Authentication** - Secure the API
6. **Deploy** - Deploy to a server (Heroku, AWS, etc.)

## Keep the Server Running!

Remember: Keep the terminal with the server running open. If you close it, the server stops.

To stop the server: Press `CTRL + C` in the terminal
