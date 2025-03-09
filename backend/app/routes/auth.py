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
    Mock login that checks 'mock_log_in' for matching credentials
    and returns the corresponding 'pymes_trust' record with a mock token.
    """
    user_login = db.query(MockLogIn).filter(
        MockLogIn.ruc == login_req.ruc,
        MockLogIn.password == login_req.password
    ).first()
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_profile = db.query(PymeTrust).filter(
        PymeTrust.ruc == login_req.ruc
    ).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User not found in pymes_trust")

    return LoginResponse(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier,
        token="mock-token"  # In real scenarios, use JWT or similar
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


