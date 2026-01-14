"""Test script to verify dashboard route"""
from app.main import app

# Get all routes
routes = []
for route in app.routes:
    if hasattr(route, 'path'):
        methods = list(route.methods) if hasattr(route, 'methods') else []
        routes.append((route.path, methods))

print("All registered routes:")
print("=" * 60)
for path, methods in sorted(routes):
    print(f"{path:40} {methods}")

print("\n" + "=" * 60)
print("Checking for /dashboard route:")
dashboard_routes = [r for r in routes if '/dashboard' in r[0]]
if dashboard_routes:
    print("✓ Dashboard route found:")
    for path, methods in dashboard_routes:
        print(f"  {path} - {methods}")
else:
    print("✗ Dashboard route NOT found!")

# Test if we can get the route function
try:
    from app.main import dashboard
    print("\n✓ Dashboard function exists and is importable")
except Exception as e:
    print(f"\n✗ Error importing dashboard: {e}")
