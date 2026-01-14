
from pydantic import BaseModel
from typing import Optional, List

class DiseaseReport(BaseModel):
    animal_id: str
    location: str
    symptoms: str
    severity: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    clinical_signs: Optional[List[str]] = None