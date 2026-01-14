"""
API Routes for Path of Least Risk
Member 2: Full-Stack Developer
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.services.path_of_least_risk import PathOfLeastRisk, initialize_cameroon_network
from pydantic import BaseModel

router = APIRouter()

# Initialize the system (singleton pattern)
_path_system: Optional[PathOfLeastRisk] = None

def get_path_system() -> PathOfLeastRisk:
    """Get or create the Path of Least Risk system."""
    global _path_system
    if _path_system is None:
        _path_system = initialize_cameroon_network()
    return _path_system


class OutbreakReport(BaseModel):
    location: str
    severity: int
    disease: str
    connected_locations: Optional[List[str]] = None


class RouteRequest(BaseModel):
    start: str
    end: str


@router.post("/outbreak")
def report_outbreak(report: OutbreakReport):
    """
    Report a disease outbreak and update the network.
    """
    system = get_path_system()
    
    try:
        system.report_outbreak(
            location=report.location,
            severity=report.severity,
            disease=report.disease,
            connected_locations=report.connected_locations
        )
        
        return {
            "status": "outbreak_reported",
            "location": report.location,
            "clusters": system.get_clusters()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/clusters")
def get_clusters():
    """Get all outbreak clusters."""
    system = get_path_system()
    return {"clusters": system.get_clusters()}


@router.get("/clusters/{location}")
def get_cluster_for_location(location: str):
    """Get cluster for a specific location."""
    system = get_path_system()
    cluster = system.get_cluster_for_location(location)
    return {"location": location, "cluster": cluster}


@router.post("/route")
def calculate_safest_route(request: RouteRequest):
    """
    Calculate the safest route between two locations.
    """
    system = get_path_system()
    
    try:
        path, total_risk = system.calculate_safest_route(request.start, request.end)
        
        if not path:
            raise HTTPException(status_code=404, detail="No route found")
        
        return {
            "start": request.start,
            "end": request.end,
            "path": path,
            "total_risk": total_risk,
            "path_length": len(path) - 1
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/routes/{start}")
def get_all_routes_from(start: str):
    """Get safest routes from a location to all other locations."""
    system = get_path_system()
    
    try:
        routes = system.get_all_safest_routes(start)
        return {
            "start": start,
            "routes": {
                dest: {
                    "path": path,
                    "total_risk": risk
                }
                for dest, (path, risk) in routes.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/outbreaks")
def get_outbreaks():
    """Get all active outbreaks."""
    system = get_path_system()
    outbreaks = system.get_outbreak_locations()
    outbreak_info = {
        loc: system.get_outbreak_info(loc)
        for loc in outbreaks
    }
    return {"outbreaks": outbreak_info}
