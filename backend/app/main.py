# app/main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from uuid import uuid4
from datetime import datetime
from app.models import UserProfile, LoginRequest, LoginResponse, OptInRequest

# Simulated in-memory database
fake_db = {}

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

# --- Mock Authentication Function ---
def authenticate_user(username: str, password: str) -> str:
    """
    In production, you'd verify credentials against Banco de Guayaquil's auth system.
    For this MVP, we simply generate a UUID for any login.
    """
    return str(uuid4())

# --- API Endpoints ---

@app.post("/login", response_model=LoginResponse, tags=["Authentication"], summary="User Login")
def login(login_req: LoginRequest):
    user_id = authenticate_user(login_req.username, login_req.password)
    # Create a new user profile if not existing
    if user_id not in fake_db:
        fake_db[user_id] = UserProfile(
            user_id=user_id,
            company_name=f"Company_{user_id[:5]}",
            opted_in=False,
        )
    # Return a mock token; in production, use JWT or similar
    return LoginResponse(user_id=user_id, token="mock-token")


@app.get("/profile/{user_id}", response_model=UserProfile, tags=["User Profile"], summary="Get User Profile")
def get_profile(user_id: str):
    profile = fake_db.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile


@app.post("/opt-in", tags=["User Profile"], summary="User Opt-In/Out")
def opt_in(opt_req: OptInRequest):
    profile = fake_db.get(opt_req.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    profile.opted_in = opt_req.opt_in
    fake_db[opt_req.user_id] = profile
    return {
        "message": f"User has {'opted in' if opt_req.opt_in else 'opted out'} successfully."
    }


@app.post("/recalculate_category/{user_id}", tags=["User Categorization"], summary="Recalculate User Category")
def recalculate_category(user_id: str, background_tasks: BackgroundTasks):
    profile = fake_db.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    # Add background task for user categorization
    background_tasks.add_task(categorize_user, user_id)
    return {"message": "Category recalculation initiated."}


def categorize_user(user_id: str):
    """
    Background task function that fetches data from external APIs (mocked) 
    and assigns a new tier to the user profile.
    """
    import time
    from app.tasks import fetch_and_calculate_category

    # Simulate processing delay
    time.sleep(1)

    # Calculate new tier & badge
    new_tier, badge_url = fetch_and_calculate_category(user_id)
    profile = fake_db.get(user_id)
    if profile:
        profile.tier = new_tier
        profile.badge_url = badge_url
        fake_db[user_id] = profile
    print(f"User {user_id} categorized as {new_tier}")


def main():
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
