# app/routes/auth.py
from app.core.tasks import calculate_trust_score
from app.models.pymes import TierEnum
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models import MockLogIn, PymeTrust
from app.schemas import LoginRequest, LoginResponse, UserProfile

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """
    1) Accept any password (since real login is at the bank).
    2) If user (RUC) doesn't exist in mock_log_in, it's the first login:
       - Calculate trust_score & tier
       - Insert into pymes_trust
       - Insert into mock_log_in
    3) If user exists, recalc trust_score & tier in background or on-the-fly
    4) Return the user's data
    """
    existing_login = db.query(MockLogIn).filter(MockLogIn.ruc == login_req.ruc).first()

    if not existing_login:
        # First login => create a new pymes_trust record
        trust_score, tier_str = calculate_trust_score(login_req.ruc)

        new_pyme = PymeTrust(
            ruc=login_req.ruc,
            pyme_name=f"PYME_{login_req.ruc}",  # or fetch from an external source
            trust_score=trust_score,
            tier=TierEnum(tier_str)  # if using the TierEnum
        )
        db.add(new_pyme)
        db.flush()  # to get new_pyme.id if needed

        # Add to mock_log_in
        new_login = MockLogIn(
            ruc=login_req.ruc,
            password=login_req.password
        )
        db.add(new_login)
        db.commit()
        db.refresh(new_pyme)

        return LoginResponse(
            ruc=new_pyme.ruc,
            pyme_name=new_pyme.pyme_name,
            trust_score=new_pyme.trust_score,
            tier=new_pyme.tier.value if isinstance(new_pyme.tier, TierEnum) else new_pyme.tier,
            token="mock-token"
        )
    else:
        # Returning user => retrieve existing pymes_trust
        pyme = db.query(PymeTrust).filter(PymeTrust.ruc == login_req.ruc).first()
        if not pyme:
            raise HTTPException(status_code=404, detail="Data inconsistency: pymes_trust record missing.")

        # Optionally recalc trust_score & tier each login
        # (You can also do this in a background task if you prefer.)
        trust_score, tier_str = calculate_trust_score(login_req.ruc)
        pyme.trust_score = trust_score
        pyme.tier = TierEnum(tier_str)
        db.commit()
        db.refresh(pyme)

        return LoginResponse(
            ruc=pyme.ruc,
            pyme_name=pyme.pyme_name,
            trust_score=pyme.trust_score,
            tier=pyme.tier.value if isinstance(pyme.tier, TierEnum) else pyme.tier,
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


