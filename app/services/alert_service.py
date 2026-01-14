"""
Alert Service - Priority Queue Integration
Manages disease alerts based on zoonotic risk
Member 2: Full-Stack Developer
"""

from typing import List, Optional, Dict
from app.core_logic.priority_queue import PriorityQueue, Alert, ZoonoticRisk, get_risk_level
from app.schemas.report import DiseaseReport
from datetime import datetime


class AlertService:
    """
    Service for managing disease alerts using Priority Queue.
    Automatically generates alerts based on zoonotic risk levels.
    """
    
    def __init__(self):
        """Initialize the alert service."""
        self.priority_queue = PriorityQueue()
        self.alert_history: List[Alert] = []
    
    def process_report(self, report: DiseaseReport) -> Optional[Alert]:
        """
        Process a disease report and create an alert if needed.
        
        Args:
            report: Disease report
        
        Returns:
            Created alert or None if no alert needed
        """
        # Extract disease from symptoms or clinical signs
        disease = self._extract_disease(report)
        
        if not disease:
            return None
        
        # Get zoonotic risk level
        risk_level = get_risk_level(disease)
        
        # Create alert
        alert = Alert(
            disease=disease,
            location=report.location,
            risk_level=risk_level,
            details=f"Severity: {report.severity}, Symptoms: {report.symptoms}"
        )
        alert.timestamp = datetime.now().isoformat()
        
        # Add to priority queue
        self.priority_queue.push(alert)
        
        # Store in history
        self.alert_history.append(alert)
        
        return alert
    
    def _extract_disease(self, report: DiseaseReport) -> Optional[str]:
        """
        Extract disease name from report.
        
        In a real system, this would use NLP or pattern matching.
        For now, we check clinical signs against known diseases.
        """
        if report.clinical_signs:
            from app.trie_clinical_signs import build_clinical_signs_trie
            from app.clinical_signs_dict import CLINICAL_SIGNS_DICT
            
            trie = build_clinical_signs_trie(CLINICAL_SIGNS_DICT)
            
            # Get diseases for the first clinical sign
            if report.clinical_signs:
                diseases = trie.get_diseases(report.clinical_signs[0])
                if diseases:
                    return diseases[0]  # Return first matching disease
        
        # Fallback: try to extract from symptoms text
        symptoms_lower = report.symptoms.lower()
        
        # Simple keyword matching (in production, use better NLP)
        disease_keywords = {
            "anthrax": "Anthrax",
            "brucellosis": "Brucellosis",
            "tuberculosis": "Bovine Tuberculosis",
            "foot and mouth": "Foot and Mouth Disease",
            "lumpy skin": "Lumpy Skin Disease",
            "bluetongue": "Bluetongue Disease",
            "mastitis": "Mastitis",
            "ketosis": "Ketosis"
        }
        
        for keyword, disease in disease_keywords.items():
            if keyword in symptoms_lower:
                return disease
        
        return None
    
    def get_next_alert(self) -> Optional[Alert]:
        """
        Get the highest priority alert.
        
        Returns:
            Highest priority alert or None if queue is empty
        """
        return self.priority_queue.pop()
    
    def peek_next_alert(self) -> Optional[Alert]:
        """Peek at the highest priority alert without removing it."""
        return self.priority_queue.peek()
    
    def get_all_alerts(self, limit: Optional[int] = None) -> List[Alert]:
        """
        Get all alerts in priority order.
        
        Args:
            limit: Maximum number of alerts to return
        
        Returns:
            List of alerts sorted by priority
        """
        alerts = self.priority_queue.get_all_alerts()
        if limit:
            return alerts[:limit]
        return alerts
    
    def get_alerts_by_risk(self, risk_level: ZoonoticRisk) -> List[Alert]:
        """
        Get all alerts for a specific risk level.
        
        Args:
            risk_level: Risk level to filter by
        
        Returns:
            List of alerts with the specified risk level
        """
        return [alert for alert in self.alert_history if alert.risk_level == risk_level]
    
    def get_alert_count(self) -> Dict[str, int]:
        """
        Get count of alerts by risk level.
        
        Returns:
            Dictionary mapping risk level to count
        """
        counts = {
            "P1": 0,
            "P2": 0,
            "P3": 0,
            "P4": 0
        }
        
        for alert in self.alert_history:
            counts[alert.risk_level.name] += 1
        
        return counts
    
    def clear_alerts(self):
        """Clear all alerts from the queue."""
        self.priority_queue.clear()


# Global alert service instance
_alert_service: Optional[AlertService] = None

def get_alert_service() -> AlertService:
    """Get or create the alert service."""
    global _alert_service
    if _alert_service is None:
        _alert_service = AlertService()
    return _alert_service
