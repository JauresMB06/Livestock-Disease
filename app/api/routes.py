
from fastapi import APIRouter
from app.schemas.report import DiseaseReport

router = APIRouter()

@router.post("/report")
def receive_report(report: DiseaseReport):
    return {"status": "received", "data": report}
