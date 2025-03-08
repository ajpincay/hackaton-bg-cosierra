from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.db import SessionLocal, engine
from app import models_db, models
from app.tasks import fetch_and_calculate_category
import uvicorn


# Uncomment if you want SQLAlchemy to create the tables automatically.
# If your tables already exist in MySQL, you can remove or comment out.
models_db.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Banco de Guayaquil Trusted Network Backend")
# Record the startup time for health-check purposes
startup_time = datetime.utcnow()

# --- Start / Health Endpoint ---
@app.get("/", tags=["Root"], summary="Service Start Endpoint")
def read_root():
    """
    Start endpoint for Banco de Guayaquil Trusted Network Backend.
    
    This endpoint serves as a simple health check to confirm that the service
    is running. It returns a welcome message along with the service startup time.
    """
    return {
        "message": "Welcome to Banco de Guayaquil Trusted Network Backend API made by Team 'CoSierra Devs'! 🚀",
        "startup_time": startup_time.isoformat(),
    }

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/login", response_model=models.LoginResponse)
def login(login_req: models.LoginRequest, db: Session = Depends(get_db)):
    """
    Mock login endpoint that verifies credentials in mock_log_in.
    Returns the corresponding pymes_trust record plus a mock token.
    """
    user_login = db.query(models_db.MockLogIn).filter(
        models_db.MockLogIn.ruc == login_req.ruc,
        models_db.MockLogIn.password == login_req.password
    ).first()

    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Get the user profile from pymes_trust
    user_profile = db.query(models_db.PymeTrust).filter(
        models_db.PymeTrust.ruc == login_req.ruc
    ).first()

    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return models.LoginResponse(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier,
        token="mock-token"
    )

@app.get("/profile/{ruc}", response_model=models.UserProfile)
def get_profile(ruc: str, db: Session = Depends(get_db)):
    """
    Retrieve the user's pymes_trust record.
    """
    user_profile = db.query(models_db.PymeTrust).filter(
        models_db.PymeTrust.ruc == ruc
    ).first()

    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return models.UserProfile(
        ruc=user_profile.ruc,
        pyme_name=user_profile.pyme_name,
        trust_score=user_profile.trust_score,
        tier=user_profile.tier
    )

@app.post("/recalculate_category/{ruc}")
def recalculate_category(ruc: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Schedule a background task that recalculates the user's trust_score and tier.
    """
    user_profile = db.query(models_db.PymeTrust).filter(
        models_db.PymeTrust.ruc == ruc
    ).first()

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

    db = SessionLocal()
    try:
        user_profile = db.query(models_db.PymeTrust).filter(
            models_db.PymeTrust.ruc == ruc
        ).first()
        if user_profile:
            new_score, new_tier = fetch_and_calculate_category(ruc)
            user_profile.trust_score = new_score
            user_profile.tier = new_tier
            db.commit()
            print(f"User {ruc} updated to trust_score={new_score}, tier={new_tier}")
    finally:
        db.close()

# If using a custom script entry in pyproject.toml, define main() here:
def main():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
