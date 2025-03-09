# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import MockLogIn, PymeTrust
from app.schemas import LoginRequest, LoginResponse, UserProfile

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """
    Mock login that checks the mock_log_in table for (ruc, password).
    If valid, returns the matching pymes_trust record + mock token.
    """
    user_login = db.query(MockLogIn).filter(
        MockLogIn.ruc == login_req.ruc,
        MockLogIn.password == login_req.password
    ).first()
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Retrieve the user's pyme record
    user_profile = db.query(PymeTrust).filter(PymeTrust.ruc == login_req.ruc).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return LoginResponse(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier,
        token="mock-token"
    )

@router.get("/logout")
def logout():
    """
    Mock logout endpoint. In a real scenario, you'd revoke JWT or session.
    """
    return {"message": "Logged out successfully"}

@router.get("/me")
def get_current_user():
    """
    Example endpoint to get current user details if using a token-based approach.
    For the MVP, you can mock this or return static data.
    """
    return {"message": "Your user info goes here (mocked)."}

@router.get("/profile/{ruc}", response_model=UserProfile)
def get_profile(ruc: str, db: Session = Depends(get_db)):
    """
    Retrieve the user's pymes_trust record.
    """
    user_profile = (
        db.query(PymeTrust)
        .filter(PymeTrust.ruc == ruc)
        .first()
    )
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return UserProfile(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier
    )
