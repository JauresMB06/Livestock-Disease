"""
Priority Queue (Min Heap) Implementation
For managing zoonotic risk alerts
Member 1: Algorithmic Lead
"""

import heapq
from typing import List, Tuple, Optional, Any
from enum import Enum


class ZoonoticRisk(Enum):
    """
    Zoonotic risk priority levels.
    P1 = Highest risk (e.g., Anthrax)
    P4 = Lowest risk (e.g., minor parasites)
    """
    P1 = 1  # Critical - Immediate action required
    P2 = 2  # High - Urgent attention needed
    P3 = 3  # Medium - Monitor closely
    P4 = 4  # Low - Routine monitoring


class Alert:
    """Represents a disease alert with priority."""
    
    def __init__(self, disease: str, location: str, risk_level: ZoonoticRisk, 
                 details: Optional[str] = None):
        """
        Initialize an alert.
        
        Args:
            disease: Disease name
            location: Location of outbreak
            risk_level: Zoonotic risk priority
            details: Additional details
        """
        self.disease = disease
        self.location = location
        self.risk_level = risk_level
        self.details = details
        self.timestamp = None  # Can be set by external system
    
    def __lt__(self, other):
        """Compare alerts by risk level (lower priority number = higher priority)."""
        if not isinstance(other, Alert):
            return NotImplemented
        return self.risk_level.value < other.risk_level.value
    
    def __repr__(self):
        return f"Alert({self.disease}, {self.location}, {self.risk_level.name})"


class PriorityQueue:
    """
    Priority Queue (Min Heap) for managing disease alerts by zoonotic risk.
    
    Lower priority number = Higher priority (P1 is highest priority).
    
    Time Complexity:
    - push: O(log n)
    - pop: O(log n)
    - peek: O(1)
    - is_empty: O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self):
        """Initialize an empty priority queue."""
        self.heap: List[Alert] = []
        self.size = 0
    
    def push(self, alert: Alert):
        """
        Add an alert to the priority queue.
        
        Args:
            alert: Alert to add
        
        Time Complexity: O(log n)
        """
        heapq.heappush(self.heap, alert)
        self.size += 1
    
    def pop(self) -> Optional[Alert]:
        """
        Remove and return the highest priority alert.
        
        Returns:
            Highest priority alert, or None if queue is empty
        
        Time Complexity: O(log n)
        """
        if self.is_empty():
            return None
        
        self.size -= 1
        return heapq.heappop(self.heap)
    
    def peek(self) -> Optional[Alert]:
        """
        Return the highest priority alert without removing it.
        
        Returns:
            Highest priority alert, or None if queue is empty
        
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self.heap[0]
    
    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.
        
        Returns:
            True if empty, False otherwise
        
        Time Complexity: O(1)
        """
        return self.size == 0
    
    def get_size(self) -> int:
        """
        Get the number of alerts in the queue.
        
        Returns:
            Number of alerts
        
        Time Complexity: O(1)
        """
        return self.size
    
    def get_all_alerts(self) -> List[Alert]:
        """
        Get all alerts in priority order (without removing them).
        
        Returns:
            List of alerts sorted by priority
        
        Time Complexity: O(n log n) - creates sorted copy
        """
        return sorted(self.heap.copy())
    
    def clear(self):
        """Clear all alerts from the queue. O(1)"""
        self.heap.clear()
        self.size = 0


# Disease risk mapping (for reference)
DISEASE_RISK_MAP = {
    "Anthrax": ZoonoticRisk.P1,  # Critical - can infect humans
    "Brucellosis": ZoonoticRisk.P1,  # Critical - zoonotic
    "Bovine Tuberculosis": ZoonoticRisk.P1,  # Critical - zoonotic
    "Foot and Mouth Disease": ZoonoticRisk.P2,  # High - economic impact
    "Lumpy Skin Disease": ZoonoticRisk.P2,  # High - severe impact
    "Bluetongue Disease": ZoonoticRisk.P2,  # High - significant impact
    "Bovine Malignant Catarrhal Fever": ZoonoticRisk.P3,  # Medium
    "Mastitis": ZoonoticRisk.P4,  # Low - localized
    "Ketosis": ZoonoticRisk.P4,  # Low - metabolic disorder
}


def get_risk_level(disease: str) -> ZoonoticRisk:
    """
    Get the zoonotic risk level for a disease.
    
    Args:
        disease: Disease name
    
    Returns:
        ZoonoticRisk level, defaults to P3 if unknown
    """
    return DISEASE_RISK_MAP.get(disease, ZoonoticRisk.P3)


if __name__ == "__main__":
    # Example usage
    pq = PriorityQueue()
    
    # Add alerts with different priorities
    pq.push(Alert("Anthrax", "Ngaoundéré", ZoonoticRisk.P1, "Critical outbreak"))
    pq.push(Alert("Mastitis", "Maroua", ZoonoticRisk.P4, "Localized case"))
    pq.push(Alert("Foot and Mouth Disease", "Bamenda", ZoonoticRisk.P2, "Outbreak detected"))
    
    print("Processing alerts by priority:")
    while not pq.is_empty():
        alert = pq.pop()
        print(f"{alert.risk_level.name}: {alert.disease} at {alert.location}")
