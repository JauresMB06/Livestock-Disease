
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api.routes import router
from app.api.path_routes import router as path_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.alert_routes import router as alert_router

app = FastAPI(title="Livestock Disease Surveillance Network")

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Dashboard page - must be defined before other routes to avoid conflicts"""
    """Simple HTML dashboard."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Livestock Disease Surveillance Network - Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #13ec13; }
            .section { margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 5px; }
            button { padding: 10px 20px; background: #13ec13; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0ea80e; }
            input, select { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
            .result { margin-top: 10px; padding: 10px; background: #e8f5e9; border-left: 4px solid #13ec13; }
            .api-link { display: inline-block; margin: 10px 5px; padding: 8px 15px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐄 Livestock Disease Surveillance Network</h1>
            
            <div class="section">
                <h2>Quick Links</h2>
                <a href="/docs" class="api-link">API Documentation</a>
                <a href="/api/stats/summary" class="api-link">Summary Stats</a>
                <a href="/api/clusters" class="api-link">Outbreak Clusters</a>
                <a href="/api/outbreaks" class="api-link">Active Outbreaks</a>
            </div>
            
            <div class="section">
                <h2>Range Query (Segment Tree)</h2>
                <label>Start Index: <input type="number" id="start" value="0" min="0"></label>
                <label>End Index: <input type="number" id="end" value="9" min="0"></label>
                <label>Operation: 
                    <select id="operation">
                        <option value="sum">Sum</option>
                        <option value="min">Min</option>
                        <option value="max">Max</option>
                    </select>
                </label>
                <button onclick="queryRange()">Query Range</button>
                <div id="rangeResult" class="result" style="display:none;"></div>
            </div>
            
            <div class="section">
                <h2>Summary Statistics</h2>
                <button onclick="loadSummary()">Load Summary</button>
                <div id="summaryResult" class="result" style="display:none;"></div>
            </div>
        </div>
        
        <script>
            async function queryRange() {
                const start = document.getElementById('start').value;
                const end = document.getElementById('end').value;
                const op = document.getElementById('operation').value;
                
                try {
                    const response = await fetch(`/api/dashboard/stats/range?start=${start}&end=${end}&operation=${op}`);
                    const data = await response.json();
                    document.getElementById('rangeResult').style.display = 'block';
                    document.getElementById('rangeResult').innerHTML = 
                        `<strong>Result:</strong> ${data.result}<br>
                         <strong>Range:</strong> [${data.start}, ${data.end}]<br>
                         <strong>Operation:</strong> ${data.operation}`;
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            async function loadSummary() {
                try {
                    const response = await fetch('/api/dashboard/stats/summary');
                    const data = await response.json();
                    document.getElementById('summaryResult').style.display = 'block';
                    document.getElementById('summaryResult').innerHTML = 
                        `<strong>Total:</strong> ${data.total}<br>
                         <strong>Min:</strong> ${data.min}<br>
                         <strong>Max:</strong> ${data.max}<br>
                         <strong>Average:</strong> ${data.average.toFixed(2)}<br>
                         <strong>Data Points:</strong> ${data.data_points}`;
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/")
def root():
    return {"message": "LDSN API is running", "docs": "/docs", "dashboard": "/dashboard"}

app.include_router(router, prefix="/api")
app.include_router(path_router, prefix="/api/path", tags=["Path of Least Risk"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(alert_router, prefix="/api/alerts", tags=["Alerts"])


