# app/routes/auth.py
from app.core.tasks import calculate_trust_score
from app.models.pymes import TierEnum
from app.services.api_hack_bg import AsyncExternalDataService
from app.services.bedrock import bedrock_model_adjustment, get_titan_embedding
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio

from app.core.db import get_db
from app.models import MockLogIn, PymeTrust
from app.schemas import LoginRequest, LoginResponse, UserProfile

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    """
    Async login endpoint that calculates trust score and tier for a PYME.
    Uses external async API calls for trust score computation.
    """

    # Step 1: Fetch all required external data asynchronously
    persona_data = await AsyncExternalDataService.get_persona({"cedula": login_req.ruc})
    if not persona_data:
        raise HTTPException(status_code=404, detail="No user found in persona")

    persona = persona_data[0]
    if persona.get("esCliente") != 1:
        raise HTTPException(status_code=404, detail="User is not a client")

    # Step 2: Fetch multiple datasets in parallel
    salario_data, supercia_data_persona = await asyncio.gather(
        AsyncExternalDataService.get_salario({"cedula": login_req.ruc}),
        AsyncExternalDataService.get_supercia({"cedula": login_req.ruc})
    )

    in_salario = bool(salario_data)
    in_supercia = bool(supercia_data_persona)

    # Step 3: Special case check: if salario's rucEmpresa exists in supercia
    special_case = False
    special_ruc = None
    special_nombreEmpresa = None

    if in_salario:
        for rec in salario_data:
            supercia_data_empresa = await AsyncExternalDataService.get_supercia({"cedula": rec.get("rucEmpresa")})
            if supercia_data_empresa:
                special_case = True
                special_ruc = rec.get("rucEmpresa")
                special_nombreEmpresa = rec.get("nombreEmpresa")
                break

    # Step 4: Determine final PYME trust values
    final_ruc = special_ruc if special_case else login_req.ruc
    final_pyme_name = (special_nombreEmpresa[:35] if special_case 
                       else f"{persona.get('nombres', '')}_{persona.get('apellidos', '')} S.A.")[:35]

    # Step 5: Fetch remaining data asynchronously
    auto_data, establecimiento_data, scoreburo_data = await asyncio.gather(
        AsyncExternalDataService.get_auto({"cedula": login_req.ruc}),
        AsyncExternalDataService.get_establecimiento({"cedula": login_req.ruc}),
        AsyncExternalDataService.get_scoreburo({"cedula": login_req.ruc})
    )

    # Calculate trust score
    trust_score, tier_str = await calculate_trust_score(
        login_req.ruc, persona, salario_data, supercia_data_persona, auto_data, establecimiento_data, scoreburo_data
    )

    # Step 6: Handle user authentication and database updates
    existing_login = db.query(MockLogIn).filter(MockLogIn.ruc == login_req.ruc).first()
    if not existing_login:
        # First login: Create pymes_trust record and add to mock_log_in
        new_pyme = PymeTrust(
            ruc=final_ruc,
            pyme_name=final_pyme_name,
            trust_score=trust_score,
            tier=TierEnum(tier_str)  # Convert tier_str to Enum
        )
        db.add(new_pyme)
        db.flush()  # Persist before adding login

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


