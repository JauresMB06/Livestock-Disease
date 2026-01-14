"""Test server to verify dashboard works"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting test server...")
    print("Dashboard should be available at: http://127.0.0.1:8000/dashboard")
    print("Press CTRL+C to stop")
    uvicorn.run(app, host="127.0.0.1", port=8000)
