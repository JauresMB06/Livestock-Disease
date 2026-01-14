"""
Comprehensive Test Script for Livestock Disease Surveillance Network
Tests all components: Data structures, API, Dashboard, CLI, Integration
"""

import sys
import requests
import time
from typing import Dict, List

# Status indicators (using ASCII to avoid encoding issues)
PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"

def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")

def print_test(name: str, status: bool, details: str = ""):
    """Print test result."""
    status_str = PASS if status else FAIL
    print(f"  {status_str} {name}")
    if details:
        print(f"      {details}")

def test_data_structures():
    """Test all 5 data structures."""
    print_section("1. TESTING DATA STRUCTURES")
    
    results = {}
    
    # Test Graph
    try:
        from app.core_logic.graph import Graph, dijkstra, reconstruct_path
        g = Graph()
        g.add_edge("A", "B", 5.0)
        g.add_edge("A", "C", 3.0)
        distances, previous = dijkstra(g, "A")
        path = reconstruct_path(previous, "A", "B")
        results['Graph'] = (distances["B"] == 5.0 and path == ["A", "B"])
        print_test("Graph + Dijkstra", results['Graph'], f"Distance: {distances['B']}, Path: {path}")
    except Exception as e:
        results['Graph'] = False
        print_test("Graph + Dijkstra", False, f"Error: {str(e)[:50]}")
    
    # Test Union-Find
    try:
        from app.core_logic.union_find import UnionFind
        uf = UnionFind()
        uf.make_set("A")
        uf.make_set("B")
        uf.union("A", "B")
        results['Union-Find'] = uf.connected("A", "B")
        print_test("Union-Find", results['Union-Find'], f"Clusters: {uf.get_cluster_count()}")
    except Exception as e:
        results['Union-Find'] = False
        print_test("Union-Find", False, f"Error: {str(e)[:50]}")
    
    # Test Priority Queue
    try:
        from app.core_logic.priority_queue import PriorityQueue, Alert, ZoonoticRisk
        pq = PriorityQueue()
        pq.push(Alert("Anthrax", "Loc1", ZoonoticRisk.P1))
        pq.push(Alert("Mastitis", "Loc2", ZoonoticRisk.P4))
        alert = pq.pop()
        results['Priority Queue'] = (alert.risk_level == ZoonoticRisk.P1)
        print_test("Priority Queue", results['Priority Queue'], f"First alert: {alert.disease} ({alert.risk_level.name})")
    except Exception as e:
        results['Priority Queue'] = False
        print_test("Priority Queue", False, f"Error: {str(e)[:50]}")
    
    # Test Segment Tree
    try:
        from app.core_logic.segment_tree import SegmentTree
        st = SegmentTree([1, 2, 3, 4, 5], operation="sum")
        result = st.query_range(0, 2)
        results['Segment Tree'] = (result == 6.0)
        print_test("Segment Tree", results['Segment Tree'], f"Query [0,2]: {result} (expected: 6.0)")
    except Exception as e:
        results['Segment Tree'] = False
        print_test("Segment Tree", False, f"Error: {str(e)[:50]}")
    
    # Test Trie
    try:
        from app.trie_clinical_signs import build_clinical_signs_trie
        from app.clinical_signs_dict import CLINICAL_SIGNS_DICT
        trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
        results_trie = trie.search("fever")
        results['Trie'] = (len(results_trie) > 0)
        print_test("Trie", results['Trie'], f"Found {len(results_trie)} result(s) for 'fever'")
    except Exception as e:
        results['Trie'] = False
        print_test("Trie", False, f"Error: {str(e)[:50]}")
    
    return results

def test_api_endpoints(base_url: str = "http://127.0.0.1:8000"):
    """Test all API endpoints."""
    print_section("2. TESTING API ENDPOINTS")
    
    results = {}
    
    # Test root
    try:
        r = requests.get(f"{base_url}/", timeout=5)
        results['Root'] = (r.status_code == 200)
        print_test("Root endpoint", results['Root'], f"Status: {r.status_code}")
    except Exception as e:
        results['Root'] = False
        print_test("Root endpoint", False, f"Server not running or error: {str(e)[:50]}")
        return results
    
    # Test GPS endpoints
    try:
        r = requests.get(f"{base_url}/api/gps/hubs", timeout=5)
        results['GPS Hubs'] = (r.status_code == 200 and "hubs" in r.json())
        print_test("GPS Hubs", results['GPS Hubs'], f"Found {len(r.json().get('hubs', {}))} hubs")
    except Exception as e:
        results['GPS Hubs'] = False
        print_test("GPS Hubs", False, f"Error: {str(e)[:50]}")
    
    # Test Clinical Signs
    try:
        r = requests.get(f"{base_url}/api/clinical-signs/search?prefix=fever", timeout=5)
        results['Clinical Signs Search'] = (r.status_code == 200)
        print_test("Clinical Signs Search", results['Clinical Signs Search'], f"Status: {r.status_code}")
    except Exception as e:
        results['Clinical Signs Search'] = False
        print_test("Clinical Signs Search", False, f"Error: {str(e)[:50]}")
    
    # Test Dashboard
    try:
        r = requests.get(f"{base_url}/dashboard", timeout=5)
        results['Dashboard'] = (r.status_code == 200 and "<html" in r.text.lower())
        print_test("Dashboard", results['Dashboard'], f"Status: {r.status_code}, HTML: {'Yes' if '<html' in r.text.lower() else 'No'}")
    except Exception as e:
        results['Dashboard'] = False
        print_test("Dashboard", False, f"Error: {str(e)[:50]}")
    
    # Test Path of Least Risk
    try:
        r = requests.get(f"{base_url}/api/path/clusters", timeout=5)
        results['Path Clusters'] = (r.status_code == 200)
        print_test("Path Clusters", results['Path Clusters'], f"Status: {r.status_code}")
    except Exception as e:
        results['Path Clusters'] = False
        print_test("Path Clusters", False, f"Error: {str(e)[:50]}")
    
    # Test Alerts
    try:
        r = requests.get(f"{base_url}/api/alerts/stats", timeout=5)
        results['Alerts Stats'] = (r.status_code == 200)
        print_test("Alerts Stats", results['Alerts Stats'], f"Status: {r.status_code}")
    except Exception as e:
        results['Alerts Stats'] = False
        print_test("Alerts Stats", False, f"Error: {str(e)[:50]}")
    
    # Test Dashboard Segment Tree
    try:
        r = requests.get(f"{base_url}/api/dashboard/stats/range?start=0&end=9&operation=sum", timeout=5)
        results['Dashboard Range Query'] = (r.status_code == 200)
        print_test("Dashboard Range Query", results['Dashboard Range Query'], f"Status: {r.status_code}, Result: {r.json().get('result', 'N/A')}")
    except Exception as e:
        results['Dashboard Range Query'] = False
        print_test("Dashboard Range Query", False, f"Error: {str(e)[:50]}")
    
    return results

def test_integration():
    """Test integration features."""
    print_section("3. TESTING INTEGRATION FEATURES")
    
    results = {}
    
    # Test Path of Least Risk
    try:
        from app.services.path_of_least_risk import initialize_cameroon_network
        system = initialize_cameroon_network()
        system.report_outbreak("Ngaoundéré", severity=3, disease="Anthrax")
        path, risk = system.calculate_safest_route("Maroua", "Bamenda")
        results['Path of Least Risk'] = (len(path) > 0)
        print_test("Path of Least Risk", results['Path of Least Risk'], f"Path: {' -> '.join(path)}, Risk: {risk}")
    except Exception as e:
        results['Path of Least Risk'] = False
        print_test("Path of Least Risk", False, f"Error: {str(e)[:50]}")
    
    # Test Alert Service
    try:
        from app.services.alert_service import get_alert_service
        from app.schemas.report import DiseaseReport
        service = get_alert_service()
        report = DiseaseReport(
            animal_id="COW001",
            location="Ngaoundéré",
            symptoms="Anthrax detected",
            severity=5,
            clinical_signs=["fever"]
        )
        alert = service.process_report(report)
        results['Alert Service'] = (alert is not None)
        print_test("Alert Service", results['Alert Service'], f"Alert created: {alert.disease if alert else 'None'}")
    except Exception as e:
        results['Alert Service'] = False
        print_test("Alert Service", False, f"Error: {str(e)[:50]}")
    
    return results

def test_unit_tests():
    """Run unit tests."""
    print_section("4. RUNNING UNIT TESTS")
    
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_data_structures.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Count passing tests
        output = result.stdout
        passed = output.count("PASSED")
        failed = output.count("FAILED")
        
        print_test("Unit Tests", failed == 0, f"Passed: {passed}, Failed: {failed}")
        
        if failed > 0:
            print(f"\n    {INFO} Test failures detected. Check output above.")
        
        return {"Unit Tests": failed == 0, "Passed": passed, "Failed": failed}
    except Exception as e:
        print_test("Unit Tests", False, f"Error running tests: {str(e)[:50]}")
        return {"Unit Tests": False}

def main():
    """Run all tests."""
    print("\n" + "="*70)
    print("LIVESTOCK DISEASE SURVEILLANCE NETWORK - COMPREHENSIVE TEST")
    print("="*70)
    
    all_results = {}
    
    # Test 1: Data Structures
    ds_results = test_data_structures()
    all_results.update(ds_results)
    
    # Test 2: API Endpoints (check if server is running first)
    print(f"\n{INFO} Checking if server is running...")
    try:
        r = requests.get("http://127.0.0.1:8000/", timeout=2)
        api_results = test_api_endpoints()
        all_results.update(api_results)
    except:
        print(f"\n{FAIL} Server is not running!")
        print(f"{INFO} Start server with: uvicorn app.main:app --reload")
        print(f"{INFO} Skipping API endpoint tests...")
    
    # Test 3: Integration
    integration_results = test_integration()
    all_results.update(integration_results)
    
    # Test 4: Unit Tests
    unit_results = test_unit_tests()
    all_results.update(unit_results)
    
    # Summary
    print_section("TEST SUMMARY")
    
    # Filter out non-test entries
    test_results = {k: v for k, v in all_results.items() if k not in ["Passed", "Failed"]}
    total = len(test_results)
    
    passed_count = 0
    for name, result in test_results.items():
        if isinstance(result, dict):
            if "Unit Tests" in result:
                if result["Unit Tests"]:
                    passed_count += 1
        elif result is True:
            passed_count += 1
    
    failed_count = total - passed_count
    
    print(f"\nTotal Tests: {total}")
    print(f"{PASS} Passed: {passed_count}")
    print(f"{FAIL} Failed: {failed_count}")
    print(f"Success Rate: {(passed_count/total*100):.1f}%")
    
    # Detailed results
    print(f"\nDetailed Results:")
    for name, result in test_results.items():
        if isinstance(result, dict):
            if "Unit Tests" in result:
                status = result["Unit Tests"]
                details = f"({result.get('Passed', 0)} passed, {result.get('Failed', 0)} failed)"
            else:
                status = result.get("status", False)
                details = ""
        else:
            status = result
            details = ""
        
        status_icon = PASS if status else FAIL
        print(f"  {status_icon} {name} {details}")
    
    print("\n" + "="*70)
    
    if failed_count == 0:
        print(f"{PASS} ALL TESTS PASSED! Everything is working correctly!")
    else:
        print(f"{INFO} Some tests failed. Check the output above for details.")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
