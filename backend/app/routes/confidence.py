# routes/confidence.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.pymes import PymeTrust
from app.schemas.pymes import ConfidenceResponse, ConfidenceDetail

router = APIRouter()

@router.get("/{ruc}", response_model=ConfidenceResponse)
def get_confidence_details(ruc: str, db: Session = Depends(get_db)):
    """
    Shows how the trust score is broken down by various factors
    (financial health, reputation, digital presence, etc.).
    For demonstration, we'll just mock the breakdown.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    # Mock breakdown
    breakdown = [
        ConfidenceDetail(factor_name="Financial Health", value=30.0, weight=0.4),
        ConfidenceDetail(factor_name="Business Reputation", value=20.0, weight=0.25),
        ConfidenceDetail(factor_name="Digital Presence", value=15.0, weight=0.20),
        ConfidenceDetail(factor_name="Legal Status", value=10.0, weight=0.10),
        ConfidenceDetail(factor_name="Web/SEO Metrics", value=5.0, weight=0.05),
    ]

    total_score = sum(d.value for d in breakdown)  # 80 in this mock
    # Convert total_score to tier if you like, or use pyme.tier
    return ConfidenceResponse(
        total_score=total_score,
        tier=pyme.tier,
        breakdown=breakdown
    )
