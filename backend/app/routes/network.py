# routes/network.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.pymes import PymeTrust
from app.schemas.pymes import NetworkResponse, NetworkRecommendation

router = APIRouter()

@router.get("/recommendations/{ruc}", response_model=NetworkResponse)
def get_recommendations(ruc: str, db: Session = Depends(get_db)):
    """
    Suggest potential B2B connections for the given PYME.
    For demonstration, we simply return all PYMEs with a mock 'compatibility_score'.
    In production, you might implement AI/embeddings logic here.
    """
    current_pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not current_pyme:
        # Return an empty list or raise an error
        return NetworkResponse(recommendations=[])

    # Example: get all other pymes
    all_pymes = db.query(PymeTrust).filter(PymeTrust.ruc != ruc).all()

    # Mock "compatibility_score" as a function of trust scores
    recommendations = []
    for pyme in all_pymes:
        compatibility = abs(pyme.trust_score - current_pyme.trust_score) / 100.0
        # The smaller the difference, the higher the compatibility
        rec = NetworkRecommendation(
            ruc=pyme.ruc,
            pyme_name=pyme.pyme_name,
            trust_score=pyme.trust_score,
            tier=pyme.tier,
            compatibility_score=1.0 - compatibility
        )
        recommendations.append(rec)

    # Sort by highest compatibility first
    recommendations.sort(key=lambda x: x.compatibility_score, reverse=True)
    return NetworkResponse(recommendations=recommendations)
