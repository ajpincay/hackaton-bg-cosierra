# routes/network.py
from app.models.pymes import PeerPymesTrustScore, PymeConnection, PymeTrust
from app.schemas.pymes import NetworkResponse, NetworkRecommendation, PymeView, PeerReviewCreate
from app.services.external_data import AsyncExternalDataService
from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import get_db
import asyncio

router = APIRouter()

@router.get("/{ruc}", response_model=list[PymeView])
async def get_all_pymes(ruc: str, db: Session = Depends(get_db)):
    """
    Returns all PYMEs in the network, except the one with the given RUC.
    Uses batch fetching for salario and establecimiento data to improve performance.
    """
    pymes = db.query(PymeTrust).filter(PymeTrust.ruc != ruc).all()
    recommendations = []

    # Extract all RUCs from the PYMEs
    all_rucs = [pyme.ruc for pyme in pymes]

    # Fetch sector and location data in parallel using batch methods
    salario_results, establecimiento_results = await asyncio.gather(
        AsyncExternalDataService.get_salario_batch(all_rucs),
        AsyncExternalDataService.get_establecimiento_batch(all_rucs)
    )

    # Convert results into dictionaries for O(1) lookup
    sector_map = {
        ruc: data[0].get("sector", "Unknown") if isinstance(data, list) and data else "Unknown"
        for ruc, data in salario_results.items()
    }

    location_map = {
        ruc: data[0].get("provincia", "Unknown") if isinstance(data, list) and data else "Unknown"
        for ruc, data in establecimiento_results.items()
    }

    for pyme in pymes:
        # Obtain peer review score (average of all reviews received by this PyME)
        peer_review = db.query(func.avg(PeerPymesTrustScore.peer_trust_score))\
                        .filter(PeerPymesTrustScore.score_receiver == pyme.ruc)\
                        .scalar() or 0  # Default to 0 if no reviews exist

        # Get sector & location from pre-fetched data
        sector = sector_map.get(pyme.ruc, "Unknown")
        location = location_map.get(pyme.ruc, "Unknown")

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


@router.get("/reviews/{ruc}")
def get_peer_reviews(ruc: str, db: Session = Depends(get_db)):
    """
    Retrieve all peer reviews for a given PyME.
    """
    reviews = db.query(PeerPymesTrustScore).filter(PeerPymesTrustScore.score_receiver == ruc).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this PyME")

    return {"reviews": reviews}

@router.post("/review/{reviewer_ruc}/{reviewed_ruc}")
def submit_peer_review(reviewer_ruc: str, reviewed_ruc: str, review: PeerReviewCreate, db: Session = Depends(get_db)):
    """
    Allows one PyME to review another PyME, assigning a score (1-10).
    """
    if reviewer_ruc == reviewed_ruc:
        raise HTTPException(status_code=400, detail="Cannot review yourself")

    if not (1 <= review.peer_trust_score <= 10):
        raise HTTPException(status_code=400, detail="Score must be between 1 and 10")

    new_review = PeerPymesTrustScore(
        score_issuer=reviewer_ruc,
        score_receiver=reviewed_ruc,
        peer_trust_score=review.peer_trust_score
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {"message": "Review submitted successfully", "review": new_review}


@router.post("/reject/{requester_ruc}/{receiver_ruc}")
def reject_connection(requester_ruc: str, receiver_ruc: str, db: Session = Depends(get_db)):
    """
    Reject a pending connection request.
    """
    connection = db.query(PymeConnection).filter(
        (PymeConnection.requester_ruc == requester_ruc) & (PymeConnection.receiver_ruc == receiver_ruc),
        PymeConnection.status == "Pending"
    ).first()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection request not found")

    connection.status = "Rejected"
    db.commit()
    return {"message": "Connection rejected"}

@router.post("/accept/{requester_ruc}/{receiver_ruc}")
def accept_connection(requester_ruc: str, receiver_ruc: str, db: Session = Depends(get_db)):
    """
    Accept a pending connection request.
    """
    connection = db.query(PymeConnection).filter(
        (PymeConnection.requester_ruc == requester_ruc) & (PymeConnection.receiver_ruc == receiver_ruc),
        PymeConnection.status == "Pending"
    ).first()

    if not connection:
        raise HTTPException(status_code=404, detail="Connection request not found")

    connection.status = "Accepted"
    db.commit()
    return {"message": "Connection accepted"}

@router.post("/connect/{requester_ruc}/{receiver_ruc}")
def request_connection(requester_ruc: str, receiver_ruc: str, db: Session = Depends(get_db)):
    """
    Request a connection between two PYMEs.
    """
    if requester_ruc == receiver_ruc:
        raise HTTPException(status_code=400, detail="Cannot connect to yourself")

    existing_connection = db.query(PymeConnection).filter(
        ((PymeConnection.requester_ruc == requester_ruc) & (PymeConnection.receiver_ruc == receiver_ruc)) |
        ((PymeConnection.requester_ruc == receiver_ruc) & (PymeConnection.receiver_ruc == requester_ruc))
    ).first()

    if existing_connection:
        raise HTTPException(status_code=400, detail="Connection already exists")

    new_connection = PymeConnection(
        requester_ruc=requester_ruc,
        receiver_ruc=receiver_ruc,
        status="Pending"
    )
    db.add(new_connection)
    db.commit()
    db.refresh(new_connection)
    return {"message": "Connection request sent", "connection": new_connection}
