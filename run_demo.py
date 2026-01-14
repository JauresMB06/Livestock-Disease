"""
Demo script to test the integrated Livestock Disease Surveillance Network
Combines GPS coordinates, Clinical Signs Trie, and FastAPI backend
"""

import requests
import json
from app.gps_coordinates import get_all_hubs, format_coordinates
from app.clinical_signs_dict import CLINICAL_SIGNS_DICT, get_all_clinical_signs
from app.trie_clinical_signs import build_clinical_signs_trie

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def demo_gps_coordinates():
    """Demonstrate GPS coordinates functionality."""
    print_section("GPS COORDINATES FOR CAMEROONIAN CATTLE HUBS")
    
    hubs = get_all_hubs()
    for city, data in hubs.items():
        print(f"\n{city}:")
        print(f"  Latitude:  {data['latitude']}°N")
        print(f"  Longitude: {data['longitude']}°E")
        print(f"  Region:    {data['region']}")
        print(f"  Country:   {data['country']}")

def demo_clinical_signs():
    """Demonstrate clinical signs dictionary and Trie."""
    print_section("CLINICAL SIGNS DICTIONARY & TRIE")
    
    print(f"\nTotal diseases: {len(CLINICAL_SIGNS_DICT)}")
    print(f"Total unique clinical signs: {len(get_all_clinical_signs())}")
    
    # Build Trie
    trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
    print("\n[OK] Clinical Signs Trie built successfully!")
    
    # Test searches
    print("\nTrie Search Examples:")
    search_terms = ["fever", "lameness", "swelling"]
    
    for term in search_terms:
        results = trie.search(term)
        print(f"\n  Searching for '{term}': Found {len(results)} result(s)")
        for result in results[:2]:  # Show first 2
            print(f"    - {result['clinical_sign']}")
            if result['diseases']:
                print(f"      Diseases: {', '.join(result['diseases'][:2])}")

def demo_api_endpoints(base_url="http://127.0.0.1:8000"):
    """Demonstrate API endpoints (requires server to be running)."""
    print_section("API ENDPOINTS DEMONSTRATION")
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test GPS hubs endpoint
        print("\n2. Testing GPS hubs endpoint...")
        response = requests.get(f"{base_url}/api/gps/hubs")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            hubs = response.json()["hubs"]
            print(f"   Found {len(hubs)} cattle hubs")
        
        # Test specific hub
        print("\n3. Testing specific hub (Ngaoundéré)...")
        response = requests.get(f"{base_url}/api/gps/hubs/Ngaoundéré")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Coordinates: {response.json()}")
        
        # Test clinical signs search
        print("\n4. Testing clinical signs search (prefix: 'fever')...")
        response = requests.get(f"{base_url}/api/clinical-signs/search?prefix=fever")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {data['count']} clinical sign(s) matching 'fever'")
        
        # Test disease report
        print("\n5. Testing disease report submission...")
        report_data = {
            "animal_id": "COW001",
            "location": "Ngaoundéré",
            "symptoms": "High fever, nasal discharge",
            "severity": 3,
            "clinical_signs": ["fever", "nasal discharge"]
        }
        response = requests.post(f"{base_url}/api/report", json=report_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Report received!")
            if result.get("associated_diseases"):
                print(f"   Associated diseases: {', '.join(result['associated_diseases'][:3])}")
            if result.get("gps_coordinates"):
                print(f"   GPS: {result['gps_coordinates']}")
        
    except requests.exceptions.ConnectionError:
        print("\n[WARNING] API server is not running!")
        print("   Start the server with: uvicorn app.main:app --reload")
        print("   Then run this demo again to test API endpoints.")

def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("LIVESTOCK DISEASE SURVEILLANCE NETWORK - INTEGRATED DEMO")
    print("=" * 70)
    
    # Demo GPS coordinates
    demo_gps_coordinates()
    
    # Demo clinical signs
    demo_clinical_signs()
    
    # Demo API (if server is running)
    demo_api_endpoints()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print("\nTo start the API server, run:")
    print("  cd Livestock-Disease")
    print("  uvicorn app.main:app --reload")
    print("\nThen test the API endpoints at: http://127.0.0.1:8000/docs")
    print("=" * 70)

if __name__ == "__main__":
    main()
