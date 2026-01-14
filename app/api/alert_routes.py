"""
Alert API Routes
Priority Queue integration for alerts
Member 2: Full-Stack Developer
"""

from fastapi import APIRouter
from typing import Optional
from app.services.alert_service import get_alert_service
from app.core_logic.priority_queue import ZoonoticRisk

router = APIRouter()


@router.get("/next")
def get_next_alert():
    """Get the highest priority alert."""
    alert_service = get_alert_service()
    alert = alert_service.get_next_alert()
    
    if not alert:
        return {"message": "No alerts in queue"}
    
    return {
        "disease": alert.disease,
        "location": alert.location,
        "risk_level": alert.risk_level.name,
        "priority": alert.risk_level.value,
        "details": alert.details,
        "timestamp": alert.timestamp
    }


@router.get("/peek")
def peek_next_alert():
    """Peek at the highest priority alert without removing it."""
    alert_service = get_alert_service()
    alert = alert_service.peek_next_alert()
    
    if not alert:
        return {"message": "No alerts in queue"}
    
    return {
        "disease": alert.disease,
        "location": alert.location,
        "risk_level": alert.risk_level.name,
        "priority": alert.risk_level.value,
        "details": alert.details,
        "timestamp": alert.timestamp
    }


@router.get("/all")
def get_all_alerts(limit: Optional[int] = None):
    """Get all alerts in priority order."""
    alert_service = get_alert_service()
    alerts = alert_service.get_all_alerts(limit=limit)
    
    return {
        "alerts": [
            {
                "disease": alert.disease,
                "location": alert.location,
                "risk_level": alert.risk_level.name,
                "priority": alert.risk_level.value,
                "details": alert.details,
                "timestamp": alert.timestamp
            }
            for alert in alerts
        ],
        "count": len(alerts)
    }


@router.get("/by-risk/{risk_level}")
def get_alerts_by_risk(risk_level: str):
    """Get alerts filtered by risk level (P1, P2, P3, P4)."""
    try:
        risk_enum = ZoonoticRisk[risk_level.upper()]
    except KeyError:
        return {"error": f"Invalid risk level: {risk_level}. Use P1, P2, P3, or P4"}
    
    alert_service = get_alert_service()
    alerts = alert_service.get_alerts_by_risk(risk_enum)
    
    return {
        "risk_level": risk_level,
        "alerts": [
            {
                "disease": alert.disease,
                "location": alert.location,
                "details": alert.details,
                "timestamp": alert.timestamp
            }
            for alert in alerts
        ],
        "count": len(alerts)
    }


@router.get("/stats")
def get_alert_stats():
    """Get alert statistics by risk level."""
    alert_service = get_alert_service()
    counts = alert_service.get_alert_count()
    
    return {
        "total_alerts": sum(counts.values()),
        "by_risk_level": counts,
        "queue_size": alert_service.priority_queue.get_size()
    }
