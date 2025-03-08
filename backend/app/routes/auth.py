from app.models import pymes as models_db
from app.schemas import pymes as models
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db

router = APIRouter()

@router.post("/login", response_model=models.LoginResponse)
def login(login_req: models.LoginRequest, db: Session = Depends(get_db)):
    """
    Mock login endpoint that verifies credentials and returns a mock token.
    """
    user_login = (
        db.query(models_db.MockLogIn)
        .filter(
            models_db.MockLogIn.ruc == login_req.ruc,
            models_db.MockLogIn.password == login_req.password
        )
        .first()
    )
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_profile = (
        db.query(models_db.PymeTrust)
        .filter(models_db.PymeTrust.ruc == login_req.ruc)
        .first()
    )
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return models.LoginResponse(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier,
        token="mock-token"
    )

@router.get("/profile/{ruc}", response_model=models.UserProfile)
def get_profile(ruc: str, db: Session = Depends(get_db)):
    """
    Retrieve the user's pymes_trust record.
    """
    user_profile = (
        db.query(models_db.PymeTrust)
        .filter(models_db.PymeTrust.ruc == ruc)
        .first()
    )
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return models.UserProfile(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier
    )
