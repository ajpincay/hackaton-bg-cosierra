from app.core.sme_metrics import FinancialMetrics
from app.services.business_reputation import BusinessAnalysisService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.pymes import PymeTrust
from app.schemas.pymes import ConfidenceResponse, ConfidenceDetail
from app.services.external_data import AsyncExternalDataService

router = APIRouter()

@router.get("/{ruc}", response_model=ConfidenceResponse)
async def get_confidence_details(ruc: str, db: Session = Depends(get_db)):
    """
    Fetches a detailed confidence score breakdown using real data sources.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")
    
    # Retrieve real financial data
    raw_data = await AsyncExternalDataService.get_all_data(ruc)
    metrics = FinancialMetrics.calculate_metrics(raw_data)
    
    # Get AI-based analysis and embedding
    analysis_results = BusinessAnalysisService.analyze_and_embed(ruc)
    
    # Construct breakdown dynamically
    breakdown = [
        ConfidenceDetail(factor_name="Financial Health Score", value=metrics["Confidence Score"], weight=0.4),
        ConfidenceDetail(factor_name="Business Reputation", value=analysis_results["analysis"]["reputation_score"], weight=0.25),
        ConfidenceDetail(factor_name="Digital Presence", value=analysis_results["analysis"]["digital_presence_score"], weight=0.20),
        ConfidenceDetail(factor_name="Legal Status", value=analysis_results["analysis"]["legal_compliance_score"], weight=0.10),
    ]
    
    total_score = pyme.trust_score  # Retrieve total score from database
    
    return ConfidenceResponse(
        total_score=total_score,
        tier=pyme.tier,
        breakdown=breakdown
    )
