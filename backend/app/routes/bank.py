from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import PymeTrust, CreditOption, PymeCredit
from app.schemas import BankPortalData
from app.services.api_hack_bg import AsyncExternalDataService
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class CreditRequest(BaseModel):
    ruc: str
    credit_type_id: int
    amount_requested: int
    term: int

@router.get("/{ruc}", response_model=BankPortalData)
def get_bank_portal(ruc: str, db: Session = Depends(get_db)):
    """
    Returns bank-specific info for a given PYME:
      - Available credit lines
      - Application status
      - Secure messages
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")

    # Fetch available credit lines from the database
    available_credits = db.query(CreditOption).all()
    credit_lines = [credit.title for credit in available_credits]
    
    return BankPortalData(
        welcome_message=f"Welcome to BANCO DE GUAYAQUIL's portal, {pyme.pyme_name}!",
        available_credit_lines=credit_lines,
        application_status="Pending" if pyme.trust_score < 85 else "Approved",
        secure_messages=["Interest rates updated", "Please review your monthly statement"]
    )

@router.get("/list/credits")
def get_all_credits(db: Session = Depends(get_db)):
    """
    Fetches and returns all available credit types from the database.
    """
    credits = db.query(CreditOption).all()
    
    credit_list = [
        {
            "title": credit.title,
            "description": credit.description,
            "amount": credit.amount,
            "interest_rate": credit.interest_rate,
            "term": credit.term,
            "requirements": credit.requirements,
            "recommended": credit.recommended,
            "link": credit.link
        }
        for credit in credits
    ]
    
    return {"available_credits": credit_list}

@router.get("/list/credits/recommended/{ruc}")
async def get_recommended_credits(ruc: str, category: str = Query(None), db: Session = Depends(get_db)):
    """
    Fetches recommended credits for a given PYME based on its trust tier and commercial activity.
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        raise HTTPException(status_code=404, detail="PYME not found")
    
    persona_data = await AsyncExternalDataService.get_persona({"cedula": ruc})
    establecimiento_data = await AsyncExternalDataService.get_establecimiento({"cedula": ruc})
    actividad_economica = persona_data.get("actividadEconomica") or establecimiento_data.get("actividadEconomica")
    
    credits = db.query(CreditOption).all()
    recommended_credits = []
    
    for credit in credits:
        recommended = credit.recommended
        if actividad_economica and actividad_economica.lower() in credit.title.lower():
            recommended = True
        
        if category and category.lower() not in credit.title.lower():
            continue
        
        recommended_credits.append({
            "title": credit.title,
            "description": credit.description,
            "amount": credit.amount,
            "interest_rate": credit.interest_rate,
            "term": credit.term,
            "requirements": credit.requirements,
            "recommended": recommended,
            "link": credit.link
        })
    
    return {"recommended_credits": recommended_credits}

@router.post("/solicit/credit")
def solicit_credit(request: CreditRequest, db: Session = Depends(get_db)):
    """
    Endpoint to solicit a credit.
    """
    credit_type = db.query(CreditOption).filter(CreditOption.id == request.credit_type_id).first()
    if not credit_type:
        raise HTTPException(status_code=404, detail="Credit type not found")
    
    new_credit = PymeCredit(
        ruc=request.ruc,
        credit_type_id=request.credit_type_id,
        amount_approved=request.amount_requested,
        interest_rate=credit_type.interest_rate,
        term=request.term,
        start_date=date.today(),
        end_date=date.today().replace(month=date.today().month + request.term),
        progress_percentage=0,
        status="Pending"
    )
    
    db.add(new_credit)
    db.commit()
    db.refresh(new_credit)
    
    return {"message": "Credit solicitation submitted successfully", "credit_id": new_credit.id}
