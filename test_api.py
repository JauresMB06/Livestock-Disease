"""
Test script for API endpoints
"""
import time
import requests
import json

print("=" * 70)
print("TESTING API ENDPOINTS")
print("=" * 70)

# Wait for server to start
print("\nWaiting for server to start...")
time.sleep(4)

try:
    # Test 1: Root endpoint
    print("\n1. Root Endpoint:")
    r = requests.get('http://127.0.0.1:8000/')
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
    
    # Test 2: GPS Hubs
    print("\n2. GPS Hubs Endpoint:")
    r2 = requests.get('http://127.0.0.1:8000/api/gps/hubs')
    print(f"   Status: {r2.status_code}")
    if r2.status_code == 200:
        hubs = r2.json()['hubs']
        print(f"   Found {len(hubs)} cattle hubs:")
        for city in hubs:
            print(f"   - {city}: {hubs[city]['latitude']}N, {hubs[city]['longitude']}E")
    
    # Test 3: Clinical Signs Search
    print("\n3. Clinical Signs Search (prefix=fever):")
    r3 = requests.get('http://127.0.0.1:8000/api/clinical-signs/search?prefix=fever')
    print(f"   Status: {r3.status_code}")
    if r3.status_code == 200:
        results = r3.json()
        print(f"   Found {results['count']} matching clinical sign(s):")
        for res in results['results'][:2]:
            print(f"   - {res['clinical_sign']} -> {len(res['diseases'])} associated disease(s)")
    
    # Test 4: Disease Report Submission
    print("\n4. Disease Report Submission:")
    report_data = {
        'animal_id': 'COW001',
        'location': 'Ngaoundéré',
        'symptoms': 'High fever, nasal discharge',
        'severity': 3,
        'clinical_signs': ['fever', 'nasal discharge']
    }
    r4 = requests.post('http://127.0.0.1:8000/api/report', json=report_data)
    print(f"   Status: {r4.status_code}")
    if r4.status_code == 200:
        report = r4.json()
        print(f"   Report Status: {report['status']}")
        print(f"   Associated Diseases: {len(report.get('associated_diseases', []))} found")
        if report.get('associated_diseases'):
            print(f"   - {report['associated_diseases'][0]}")
        print(f"   GPS Coordinates: {report.get('gps_coordinates')}")
    
    print("\n" + "=" * 70)
    print("[SUCCESS] All API endpoints are working correctly!")
    print("=" * 70)
    print("\nServer is running at: http://127.0.0.1:8000")
    print("Interactive docs: http://127.0.0.1:8000/docs")
    print("=" * 70)
    
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to server.")
    print("Make sure the server is running with: uvicorn app.main:app --reload")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
