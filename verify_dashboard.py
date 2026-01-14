"""Verify dashboard route is working"""
import requests
import sys

def test_dashboard():
    base_url = "http://127.0.0.1:8000"
    
    print("Testing Dashboard Route...")
    print("=" * 60)
    
    # Test 1: Root endpoint
    try:
        r = requests.get(f"{base_url}/")
        print(f"1. Root endpoint: {r.status_code} - {r.json()}")
    except Exception as e:
        print(f"1. Root endpoint: ERROR - {e}")
        print("   Server might not be running!")
        return
    
    # Test 2: Dashboard endpoint
    try:
        r = requests.get(f"{base_url}/dashboard")
        print(f"2. Dashboard endpoint: {r.status_code}")
        if r.status_code == 200:
            print(f"   Content-Type: {r.headers.get('content-type')}")
            print(f"   Content Length: {len(r.text)} characters")
            if "<html" in r.text.lower():
                print("   ✓ Returns HTML content")
            else:
                print("   ✗ Does NOT return HTML")
        else:
            print(f"   Response: {r.text[:200]}")
    except Exception as e:
        print(f"2. Dashboard endpoint: ERROR - {e}")
    
    # Test 3: Docs endpoint (should work)
    try:
        r = requests.get(f"{base_url}/docs")
        print(f"3. Docs endpoint: {r.status_code}")
    except Exception as e:
        print(f"3. Docs endpoint: ERROR - {e}")
    
    print("=" * 60)
    print("\nIf dashboard returns 404:")
    print("1. Make sure server is running: uvicorn app.main:app --reload")
    print("2. Try hard refresh in browser: CTRL+F5")
    print("3. Check URL: http://127.0.0.1:8000/dashboard (no trailing slash)")

if __name__ == "__main__":
    test_dashboard()
