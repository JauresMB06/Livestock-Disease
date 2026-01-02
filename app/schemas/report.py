
from pydantic import BaseModel

class DiseaseReport(BaseModel):
    animal_id: str
    location: str
    symptoms: str
    severity: int
