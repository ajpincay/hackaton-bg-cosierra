# routes/bank.py
from app.services.banco_guayaquil_credits import BancoGuayaquilService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import PymeTrust
from app.schemas import BankPortalData

router = APIRouter()

@router.get("/{ruc}", response_model=BankPortalData)
def get_bank_portal(ruc: str, db: Session = Depends(get_db)):
    """
    Returns bank-specific info for a given PYME:
      - Available credit lines
      - Application status
      - Secure messages
      - Possibly tailored by trust_score
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    # Example logic: If trust_score >= 70 => better credit line
    if pyme.trust_score >= 70:
        credit_lines = ["Premium Credit", "SME Growth Loan"]
    else:
        credit_lines = ["Basic Credit"]

    return BankPortalData(
        welcome_message=f"Welcome to BANCO DE GUAYAQUIL's portal, {pyme.pyme_name}!",
        available_credit_lines=credit_lines,
        application_status="Pending" if pyme.trust_score < 85 else "Approved",
        secure_messages=["Interest rates updated", "Please review your monthly statement"]
    )

@router.get("/list/credits", tags=["Banco Guayaquil"])
async def get_all_credits():
    """
    Fetches and returns all available credit types from Banco Guayaquil.
    """
    try:
        credit_types = await BancoGuayaquilService.extract_credit_types()
        return {"available_credits": credit_types}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch credit types: {str(e)}")

@router.get("/list/credits/{credit_type}", tags=["Banco Guayaquil"])
async def get_credit_details(credit_type: str):
    """
    Fetches details for a specific credit type from Banco Guayaquil.
    Example: `/credits/casafacil` for detailed "Casafácil" credit info.
    """
    try:
        credit_details = await BancoGuayaquilService.get_credit_details(credit_type)
        return credit_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch credit details: {str(e)}")