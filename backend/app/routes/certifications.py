# routes/certifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.pymes import PymeTrust
from app.schemas.pymes import CertificationsResponse, CertificationData

router = APIRouter()

@router.get("/{ruc}", response_model=CertificationsResponse)
def get_certifications(ruc: str, db: Session = Depends(get_db)):
    """
    Returns a list of certifications (mocked) for a given PYME.
    In a real system, you'd store certifications in their own table.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    # Mock data
    certifications = [
        CertificationData(name="Financial Certification", status="Completed"),
        CertificationData(name="Operational Certification", status="Pending"),
    ]
    return CertificationsResponse(certifications=certifications)
