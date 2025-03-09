# routes/category.py
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import PymeTrust
from app.schemas import UserProfile
import time

router = APIRouter()

@router.post("/recalculate/{ruc}")
def recalculate_trust_score(ruc: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Schedules a background task that recalculates trust score & tier for a given PYME.
    """
    user_profile = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="PYME not found")

    background_tasks.add_task(_update_trust_score, ruc)
    return {"message": "Recalculation initiated"}

def _update_trust_score(ruc: str):
    """
    Background logic that fetches external data, calculates new score, updates DB.
    """
    from app.core.db import SessionLocal
    from app.models.pymes import PymeTrust
    from app.core.tasks import fetch_and_calculate_category

    db = SessionLocal()
    try:
        time.sleep(1)  # simulate processing delay
        pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
        if pyme:
            new_score, new_tier = fetch_and_calculate_category(ruc)
            pyme.trust_score = new_score
            pyme.tier = new_tier
            db.commit()
    finally:
        db.close()
