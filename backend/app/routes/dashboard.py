# routes/dashboard.py
from app.services.bedrock_integration import generate_financial_summary
from app.services.external_data_service import AsyncExternalDataService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import PymeTrust
from app.schemas import DashboardData

router = APIRouter()

@router.get("/{ruc}", response_model=DashboardData)
async def get_dashboard(ruc: str, db: Session = Depends(get_db)):
    """
    Returns the data needed to render the Trusted Network Dashboard:
      - Current trust score & tier
      - Mock confidence evolution
      - Recent activity feed
      - Certifications summary
      - Quick links (front-end can handle the actual links)
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    # In a real scenario, you might store 'recent activity' or 'certifications'
    # in separate tables. Here, we'll just mock them:
    mock_recent_activity = [
        "New connection request from 'Financiera Progreso'",
        "You completed 'Financial Certification' successfully"
    ]
    raw_data = await AsyncExternalDataService.get_all_data(ruc)
    #add to the raw data the trust score and tier
    raw_data['trust_score'] = pyme.trust_score
    raw_data['tier'] = str(pyme.tier)  # Convert Enum to string
    financial_summary = generate_financial_summary(raw_data)
    return DashboardData(
        trust_score=pyme.trust_score,
        tier=pyme.tier,
        recent_activity=mock_recent_activity,
        certifications_completed=1,
        certifications_pending=2,
        financial_summary=financial_summary,

    )
