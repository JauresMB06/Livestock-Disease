"""Direct test of dashboard route"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app
from fastapi.responses import HTMLResponse

# Check if route exists
dashboard_route = None
for route in app.routes:
    if hasattr(route, 'path') and route.path == '/dashboard':
        dashboard_route = route
        break

if dashboard_route:
    print("Dashboard route FOUND")
    print(f"Path: {dashboard_route.path}")
    print(f"Methods: {dashboard_route.methods}")
    print(f"Response class: {dashboard_route.response_class}")
    
    # Try to call the function directly
    try:
        from app.main import dashboard
        result = dashboard()
        print(f"\nDashboard function works!")
        print(f"Returns HTML: {isinstance(result, str) and '<html' in result}")
        print(f"Length: {len(result)} characters")
    except Exception as e:
        print(f"\nError calling dashboard function: {e}")
else:
    print("Dashboard route NOT FOUND")
