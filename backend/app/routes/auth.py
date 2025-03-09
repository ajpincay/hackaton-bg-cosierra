# app/routes/auth.py
from app.core.tasks import calculate_trust_score
from app.models.pymes import TierEnum
from app.services.external_data_service import ExternalDataService
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
    # Step 1: Query the persona endpoint using cedula = login_req.ruc
    persona_data = ExternalDataService.get_persona({"cedula": login_req.ruc})
    if not persona_data or len(persona_data) == 0:
        raise HTTPException(status_code=404, detail="No user found in persona")
    persona = persona_data[0]
    if persona.get("esCliente") != 1:
        raise HTTPException(status_code=404, detail="User is not a client")

    # Step 2: Query salario and supercia for the cedula
    salario_data = ExternalDataService.get_salario({"cedula": login_req.ruc})
    supercia_data_persona = ExternalDataService.get_supercia({"cedula": login_req.ruc})
    in_salario = salario_data is not None and len(salario_data) > 0
    in_supercia = supercia_data_persona is not None and len(supercia_data_persona) > 0

    # Step 3: Check for special case using salario's rucEmpresa in supercia
    special_case = False
    special_ruc = None
    special_nombreEmpresa = None
    if in_salario:
        for rec in salario_data:
            supercia_data_empresa = ExternalDataService.get_supercia({"cedula": rec.get("rucEmpresa")})
            if supercia_data_empresa and len(supercia_data_empresa) > 0:
                special_case = True
                special_ruc = rec.get("rucEmpresa")
                special_nombreEmpresa = rec.get("nombreEmpresa")
                break

    # Step 4: Determine final pymes_trust values
    if special_case:
        final_ruc = special_ruc
        final_pyme_name = special_nombreEmpresa[:35]
    else:
        final_ruc = login_req.ruc  # use the cedula
        constructed_name = f"{persona.get('nombres','')}_{persona.get('apellidos','')} S.A."
        final_pyme_name = constructed_name[:35]

    # Step 5: Fetch additional external data for better trust score calculation
    auto_data = ExternalDataService.get_auto({"cedula": login_req.ruc})
    establecimiento_data = ExternalDataService.get_establecimiento({"cedula": login_req.ruc})
    scoreburo_data = ExternalDataService.get_scoreburo({"cedula": login_req.ruc})
    
    # Calculate trust score and tier using external data
    trust_score, tier_str = calculate_trust_score(
        login_req.ruc, persona, salario_data, supercia_data_persona, auto_data, establecimiento_data, scoreburo_data
    )

    # Step 6: Check if the user exists in mock_log_in
    existing_login = db.query(MockLogIn).filter(MockLogIn.ruc == login_req.ruc).first()
    if not existing_login:
        # First login: Create a new pymes_trust record and add to mock_log_in
        new_pyme = PymeTrust(
            ruc=final_ruc,
            pyme_name=final_pyme_name,
            trust_score=trust_score,
            tier=TierEnum(tier_str)  # Convert tier_str ("Plata", "Oro", "Platino", "N/A") to TierEnum
        )
        db.add(new_pyme)
        db.flush()  # Ensure new_pyme is persisted before using it
        
        new_login = MockLogIn(
            ruc=login_req.ruc,
            password=login_req.password
        )
        db.add(new_login)
        db.commit()
        db.refresh(new_pyme)
        response_pyme = new_pyme
    else:
        # Returning user: update trust score and tier
        pyme = db.query(PymeTrust).filter(PymeTrust.ruc == login_req.ruc).first()
        if not pyme:
            raise HTTPException(status_code=404, detail="Inconsistency: pymes_trust record missing.")
        pyme.trust_score = trust_score
        pyme.tier = TierEnum(tier_str)
        db.commit()
        db.refresh(pyme)
        response_pyme = pyme

    return LoginResponse(
        ruc=response_pyme.ruc,
        pyme_name=response_pyme.pyme_name,
        trust_score=response_pyme.trust_score,
        tier=response_pyme.tier.value if isinstance(response_pyme.tier, TierEnum) else response_pyme.tier,
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


