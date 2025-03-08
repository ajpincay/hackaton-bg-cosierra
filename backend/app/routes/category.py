from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.tasks import fetch_and_calculate_category
from app.models import pymes as models_db

router = APIRouter()

@router.post("/recalculate/{ruc}")
def recalculate_category(ruc: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Schedule a background task to recalculate the user's trust_score and tier.
    """
    user_profile = (
        db.query(models_db.PymeTrust)
        .filter(models_db.PymeTrust.ruc == ruc)
        .first()
    )
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    background_tasks.add_task(update_category, ruc)
    return {"message": "Category recalculation initiated."}

def update_category(ruc: str):
    """
    Background task: fetch new trust_score & tier, update the DB.
    """
    import time
    time.sleep(1)  # Simulate a processing delay

    db = get_db().__next__()  # or create a fresh SessionLocal() if you prefer
    try:
        user_profile = (
            db.query(models_db.PymeTrust)
            .filter(models_db.PymeTrust.ruc == ruc)
            .first()
        )
        if user_profile:
            new_score, new_tier = fetch_and_calculate_category(ruc)
            user_profile.trust_score = new_score
            user_profile.tier = new_tier
            db.commit()
            print(f"User {ruc} updated to trust_score={new_score}, tier={new_tier}")
    finally:
        db.close()
