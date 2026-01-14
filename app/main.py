
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
            .data-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            .data-table th, .data-table td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            .data-table th { background-color: #13ec13; color: white; }
            .data-table tr:hover { background-color: #f5f5f5; }
            .cluster-item, .outbreak-item { padding: 10px; margin: 5px 0; background: #fff; border-left: 3px solid #2196F3; border-radius: 4px; }
            .no-data { padding: 20px; text-align: center; color: #666; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐄 Livestock Disease Surveillance Network</h1>
            
            <div class="section">
                <h2>Quick Links</h2>
                <a href="/docs" class="api-link">API Documentation</a>
                <button onclick="loadSummaryStats()" class="api-link" style="border: none; cursor: pointer;">Summary Stats</button>
                <button onclick="loadOutbreakClusters()" class="api-link" style="border: none; cursor: pointer;">Outbreak Clusters</button>
                <button onclick="loadActiveOutbreaks()" class="api-link" style="border: none; cursor: pointer;">Active Outbreaks</button>
            </div>
            
            <div class="section" id="quickLinksResult" style="display:none;">
                <h3 id="quickLinksTitle"></h3>
                <div id="quickLinksContent"></div>
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
            
            <div class="section">
                <h2>Test Outbreak Reporting</h2>
                <p>Create sample outbreaks to test the system:</p>
                <button onclick="createSampleOutbreak()" style="background: #ff9800;">Create Sample Outbreak</button>
                <button onclick="clearAllOutbreaks()" style="background: #f44336;">Clear All Outbreaks</button>
                <div id="outbreakTestResult" class="result" style="display:none;"></div>
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
            
            async function loadSummaryStats() {
                try {
                    const response = await fetch('/api/dashboard/stats/summary');
                    const data = await response.json();
                    const resultDiv = document.getElementById('quickLinksResult');
                    const titleDiv = document.getElementById('quickLinksTitle');
                    const contentDiv = document.getElementById('quickLinksContent');
                    
                    titleDiv.textContent = 'Summary Statistics';
                    contentDiv.innerHTML = `
                        <table class="data-table">
                            <tr><th>Metric</th><th>Value</th></tr>
                            <tr><td>Total</td><td>${data.total}</td></tr>
                            <tr><td>Minimum</td><td>${data.min}</td></tr>
                            <tr><td>Maximum</td><td>${data.max}</td></tr>
                            <tr><td>Average</td><td>${data.average.toFixed(2)}</td></tr>
                            <tr><td>Data Points</td><td>${data.data_points}</td></tr>
                        </table>
                    `;
                    resultDiv.style.display = 'block';
                } catch (error) {
                    showError('Error loading summary stats: ' + error.message);
                }
            }
            
            async function loadOutbreakClusters() {
                try {
                    const response = await fetch('/api/path/clusters');
                    const data = await response.json();
                    const resultDiv = document.getElementById('quickLinksResult');
                    const titleDiv = document.getElementById('quickLinksTitle');
                    const contentDiv = document.getElementById('quickLinksContent');
                    
                    titleDiv.textContent = 'Outbreak Clusters';
                    
                    if (!data.clusters || Object.keys(data.clusters).length === 0) {
                        contentDiv.innerHTML = '<div class="no-data">No outbreak clusters detected. All locations are currently safe.</div>';
                    } else {
                        // Clusters is a dict: {root: [locations]}
                        const clusterEntries = Object.entries(data.clusters);
                        // Filter out single-location clusters (no outbreaks)
                        const multiLocationClusters = clusterEntries.filter(([root, locations]) => locations.length > 1);
                        
                        if (multiLocationClusters.length === 0) {
                            contentDiv.innerHTML = '<div class="no-data">No outbreak clusters detected. All locations are isolated (no connected outbreaks).</div>';
                        } else {
                            let html = '<div>';
                            multiLocationClusters.forEach(([root, locations], index) => {
                                html += `
                                    <div class="cluster-item">
                                        <strong>Cluster ${index + 1}</strong><br>
                                        <strong>Root Location:</strong> ${root}<br>
                                        <strong>Connected Locations:</strong> ${locations.join(', ')}<br>
                                        <strong>Cluster Size:</strong> ${locations.length} location(s)
                                    </div>
                                `;
                            });
                            html += `</div><p><strong>Total Outbreak Clusters:</strong> ${multiLocationClusters.length}</p>`;
                            contentDiv.innerHTML = html;
                        }
                    }
                    resultDiv.style.display = 'block';
                } catch (error) {
                    showError('Error loading outbreak clusters: ' + error.message);
                }
            }
            
            async function loadActiveOutbreaks() {
                try {
                    const response = await fetch('/api/path/outbreaks');
                    const data = await response.json();
                    const resultDiv = document.getElementById('quickLinksResult');
                    const titleDiv = document.getElementById('quickLinksTitle');
                    const contentDiv = document.getElementById('quickLinksContent');
                    
                    titleDiv.textContent = 'Active Outbreaks';
                    
                    if (!data.outbreaks || Object.keys(data.outbreaks).length === 0) {
                        contentDiv.innerHTML = '<div class="no-data">No active outbreaks reported. All locations are currently safe.<br><small>Use "Test Outbreak Reporting" section below to create sample outbreaks.</small></div>';
                    } else {
                        let html = '<div>';
                        let index = 1;
                        for (const [location, info] of Object.entries(data.outbreaks)) {
                            const severity = info.severity || 0;
                            const severityColor = severity >= 4 ? '#f44336' : severity >= 3 ? '#ff9800' : '#ffc107';
                            html += `
                                <div class="outbreak-item">
                                    <strong>Outbreak #${index}</strong><br>
                                    <strong>Location:</strong> ${location}<br>
                                    <strong>Disease:</strong> ${info.disease || 'Unknown'}<br>
                                    <strong>Severity:</strong> <span style="color: ${severityColor}; font-weight: bold;">${severity}/5</span><br>
                                    <strong>Status:</strong> Active
                                </div>
                            `;
                            index++;
                        }
                        html += `</div><p><strong>Total Active Outbreaks:</strong> ${Object.keys(data.outbreaks).length}</p>`;
                        contentDiv.innerHTML = html;
                    }
                    resultDiv.style.display = 'block';
                } catch (error) {
                    showError('Error loading active outbreaks: ' + error.message);
                }
            }
            
            function showError(message) {
                const resultDiv = document.getElementById('quickLinksResult');
                const titleDiv = document.getElementById('quickLinksTitle');
                const contentDiv = document.getElementById('quickLinksContent');
                titleDiv.textContent = 'Error';
                contentDiv.innerHTML = `<div style="color: red; padding: 10px;">${message}</div>`;
                resultDiv.style.display = 'block';
            }
            
            async function createSampleOutbreak() {
                try {
                    const locations = ['Ngaoundéré', 'Maroua', 'Bamenda'];
                    const diseases = ['Anthrax', 'Foot and Mouth Disease', 'Bovine Tuberculosis'];
                    const location = locations[Math.floor(Math.random() * locations.length)];
                    const disease = diseases[Math.floor(Math.random() * diseases.length)];
                    const severity = Math.floor(Math.random() * 3) + 2; // 2-4
                    
                    const response = await fetch('/api/path/outbreak', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            location: location,
                            severity: severity,
                            disease: disease
                        })
                    });
                    
                    const data = await response.json();
                    const resultDiv = document.getElementById('outbreakTestResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = `
                        <strong>Outbreak Created!</strong><br>
                        Location: ${location}<br>
                        Disease: ${disease}<br>
                        Severity: ${severity}/5<br>
                        <button onclick="loadActiveOutbreaks(); loadOutbreakClusters();" style="margin-top: 10px; padding: 5px 10px; background: #13ec13; color: white; border: none; border-radius: 3px; cursor: pointer;">Refresh Data</button>
                    `;
                } catch (error) {
                    const resultDiv = document.getElementById('outbreakTestResult');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = `<div style="color: red;">Error: ${error.message}</div>`;
                }
            }
            
            async function clearAllOutbreaks() {
                // Note: This would require a new endpoint to clear outbreaks
                // For now, just reload the page
                if (confirm('Reload page to reset? (Outbreaks will persist until server restart)')) {
                    location.reload();
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


