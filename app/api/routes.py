
from fastapi import APIRouter
from app.schemas.report import DiseaseReport
from app.gps_coordinates import get_all_hubs, get_gps_coordinates
from app.clinical_signs_dict import CLINICAL_SIGNS_DICT, get_all_clinical_signs, get_diseases_by_sign
from app.trie_clinical_signs import build_clinical_signs_trie
from app.services.alert_service import get_alert_service

router = APIRouter()

# Initialize Trie for clinical signs
clinical_signs_trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)

@router.post("/report")
def receive_report(report: DiseaseReport):
    # If GPS coordinates are not provided but location matches a known hub, add them
    if not report.latitude or not report.longitude:
        hub_coords = get_gps_coordinates(report.location)
        if hub_coords:
            report.latitude = hub_coords["latitude"]
            report.longitude = hub_coords["longitude"]
    
    # If clinical signs are provided, search for associated diseases
    associated_diseases = []
    if report.clinical_signs:
        for sign in report.clinical_signs:
            diseases = get_diseases_by_sign(sign)
            associated_diseases.extend(diseases)
        associated_diseases = list(set(associated_diseases))  # Remove duplicates
    
    # Process alert using Priority Queue
    alert_service = get_alert_service()
    alert = alert_service.process_report(report)
    
    response = {
        "status": "received",
        "data": report,
        "associated_diseases": associated_diseases,
        "gps_coordinates": {
            "latitude": report.latitude,
            "longitude": report.longitude
        } if report.latitude and report.longitude else None
    }
    
    # Add alert information if created
    if alert:
        response["alert"] = {
            "disease": alert.disease,
            "location": alert.location,
            "risk_level": alert.risk_level.name,
            "priority": alert.risk_level.value
        }
    
    return response

@router.get("/gps/hubs")
def get_cattle_hubs():
    """Get GPS coordinates for all Cameroonian cattle hubs."""
    return {"hubs": get_all_hubs()}

@router.get("/gps/hubs/{city_name}")
def get_hub_coordinates(city_name: str):
    """Get GPS coordinates for a specific cattle hub."""
    coordinates = get_gps_coordinates(city_name)
    if coordinates:
        return coordinates
    return {"error": f"City '{city_name}' not found"}

@router.get("/clinical-signs")
def get_all_clinical_signs_endpoint():
    """Get all clinical signs from the dictionary."""
    return {"clinical_signs": get_all_clinical_signs(), "total": len(get_all_clinical_signs())}

@router.get("/clinical-signs/search")
def search_clinical_signs(prefix: str):
    """Search for clinical signs by prefix using Trie."""
    results = clinical_signs_trie.search(prefix)
    return {"prefix": prefix, "results": results, "count": len(results)}

@router.get("/clinical-signs/diseases")
def get_diseases_for_sign(sign: str):
    """Get all diseases associated with a clinical sign."""
    diseases = get_diseases_by_sign(sign)
    trie_diseases = clinical_signs_trie.get_diseases(sign)
    return {
        "clinical_sign": sign,
        "diseases": diseases,
        "trie_diseases": trie_diseases,
        "count": len(diseases)
    }

@router.get("/clinical-signs/dictionary")
def get_clinical_signs_dictionary():
    """Get the complete clinical signs dictionary."""
    return {
        "diseases": CLINICAL_SIGNS_DICT,
        "total_diseases": len(CLINICAL_SIGNS_DICT),
        "total_signs": len(get_all_clinical_signs())
    }
