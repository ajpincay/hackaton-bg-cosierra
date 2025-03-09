# routes/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.pymes import PymeTrust
from app.schemas.pymes import UserProfile

router = APIRouter()

@router.get("/{ruc}", response_model=UserProfile)
def get_profile(ruc: str, db: Session = Depends(get_db)):
    """
    Returns the PYME's detailed profile information.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    return UserProfile(
        ruc=pyme.ruc,
        pyme_name=pyme.pyme_name,
        trust_score=pyme.trust_score,
        tier=pyme.tier
    )

@router.put("/{ruc}", response_model=UserProfile)
def update_profile(ruc: str, profile_data: UserProfile, db: Session = Depends(get_db)):
    """
    Allows the PYME to update certain fields in their profile.
    For demonstration, we only allow updating pyme_name.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    pyme.pyme_name = profile_data.pyme_name
    db.commit()
    db.refresh(pyme)
    return UserProfile(
        ruc=pyme.ruc,
        pyme_name=pyme.pyme_name,
        trust_score=pyme.trust_score,
        tier=pyme.tier
    )
