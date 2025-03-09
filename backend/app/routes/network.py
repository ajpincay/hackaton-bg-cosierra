# routes/network.py
from app.services.external_data import AsyncExternalDataService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import get_db
from app.models.pymes import PeerPymesTrustScore, PymeConnection, PymeTrust
from app.schemas.pymes import NetworkResponse, NetworkRecommendation, PymeView

router = APIRouter()

@router.get("/{ruc}", response_model=list[PymeView])
async def get_all_pymes(ruc: str, db: Session = Depends(get_db)):
    """
    Returns all PYMEs in the network, except the one with the given RUC.
    """
    pymes = db.query(PymeTrust).filter(PymeTrust.ruc != ruc).all()
    recommendations = []

    salario = await AsyncExternalDataService.get_salario(params={"cedula": ruc})
    salario_data = salario[0] if isinstance(salario, list) and salario else {}

    sector = salario_data.get('sector', 'Unknown')

    # Same for `establecimiento`
    establecimiento = await AsyncExternalDataService.get_establecimiento(params={"cedula": ruc})
    establecimiento_data = establecimiento[0] if isinstance(establecimiento, list) and establecimiento else {}

    location = establecimiento_data.get('provincia', 'Unknown')

    for pyme in pymes:
        # Obtain peer review score (average of all reviews received by this PyME)
        peer_review = db.query(func.avg(PeerPymesTrustScore.peer_trust_score))\
                        .filter(PeerPymesTrustScore.score_receiver == pyme.ruc)\
                        .scalar() or 0  # Default to 0 if no reviews exist

        # Check connection status
        connection = db.query(PymeConnection).filter(
            ((PymeConnection.requester_ruc == ruc) & (PymeConnection.receiver_ruc == pyme.ruc)) |
            ((PymeConnection.requester_ruc == pyme.ruc) & (PymeConnection.receiver_ruc == ruc))
        ).first()

        connected = connection.status == "Accepted" if connection else False
        pending = connection.status == "Pending" if connection else False

        rec = PymeView(
            ruc=pyme.ruc,
            pyme_name=pyme.pyme_name,
            sector=sector,
            location=location,
            peer_review=peer_review,
            connected=connected,
            pending=pending
        )

        recommendations.append(rec)

    return recommendations

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


# endpoint to score a pyme, this will update the trust score by 1 - 10 points