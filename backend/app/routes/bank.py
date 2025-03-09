from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import PymeTrust, CreditOption, PymeCredit
from app.schemas import BankPortalData

router = APIRouter()

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

@router.get("/list/credits", tags=["Banco Guayaquil"])
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

@router.get("/list/credits/{credit_type}", tags=["Banco Guayaquil"])
def get_credit_details(credit_type: str, db: Session = Depends(get_db)):
    """
    Fetches details for a specific credit type from the database.
    """
    credit = db.query(CreditOption).filter(CreditOption.title == credit_type).first()
    if not credit:
        raise HTTPException(status_code=404, detail="Credit type not found")
    
    return {
        "title": credit.title,
        "description": credit.description,
        "amount": credit.amount,
        "interest_rate": credit.interest_rate,
        "term": credit.term,
        "requirements": credit.requirements,
        "recommended": credit.recommended,
        "link": credit.link
    }

@router.get("/list/credits/active/{ruc}", tags=["Banco Guayaquil"])
def get_active_credits(ruc: str, db: Session = Depends(get_db)):
    """
    Fetches the active credits for a given PYME, including progress percentage.
    """
    active_credits = db.query(PymeCredit).filter(
        PymeCredit.ruc == ruc, PymeCredit.status == "Active"
    ).all()
    
    if not active_credits:
        return {"message": "No active credits found"}
    
    credit_list = [
        {
            "credit_type": credit.credit_type_id,
            "amount_approved": credit.amount_approved,
            "interest_rate": credit.interest_rate,
            "term": credit.term,
            "start_date": credit.start_date,
            "end_date": credit.end_date,
            "progress_percentage": credit.progress_percentage,
            "status": credit.status
        }
        for credit in active_credits
    ]
    return {"active_credits": credit_list}

@router.get("/list/credits/completed/{ruc}", tags=["Banco Guayaquil"])
def get_completed_credits(ruc: str, db: Session = Depends(get_db)):
    """
    Fetches completed credits for a given PYME.
    """
    completed_credits = db.query(PymeCredit).filter(
        PymeCredit.ruc == ruc, PymeCredit.status == "Completed"
    ).all()
    
    if not completed_credits:
        return {"message": "No completed credits found"}
    
    credit_list = [
        {
            "credit_type": credit.credit_type_id,
            "amount_approved": credit.amount_approved,
            "interest_rate": credit.interest_rate,
            "term": credit.term,
            "start_date": credit.start_date,
            "end_date": credit.end_date,
            "status": credit.status
        }
        for credit in completed_credits
    ]
    return {"completed_credits": credit_list}