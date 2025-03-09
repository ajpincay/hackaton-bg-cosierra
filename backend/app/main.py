# app/main.py
from fastapi import FastAPI
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.db import engine
from app.models import Base

# Import routers from the routes folder
from app.routes import auth, category, external_data, dashboard, bank, certifications, confidence, network, profile

# Create the database tables if they don't already exist
#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Banco de Guayaquil Trusted Network",
    description="A backend for SMEs and entrepreneurs to access B2B services.",
    version="0.1.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Record the startup time for health-check purposes
startup_time = datetime.now(timezone.utc)

@app.get("/", tags=["Root"], summary="Health Endpoint")
def read_root():
    """
    Simple health check endpoint to confirm the service is running.
    """
    return {
        "message": "Welcome to Banco de Guayaquil Trusted Network Backend API made by Team 'CoSierra Devs'! 🚀",
        "startup_time": startup_time.isoformat(),
    }

# Include the routers from separate files
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(category.router, prefix="/category", tags=["Category"])
app.include_router(external_data.router, prefix="/external", tags=["ExternalData"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(bank.router, prefix="/bank", tags=["Bank"])
app.include_router(certifications.router, prefix="/certifications", tags=["Certifications"])
app.include_router(confidence.router, prefix="/confidence", tags=["Confidence"])
app.include_router(network.router, prefix="/network", tags=["Network"])
app.include_router(profile.router, prefix="/profile", tags=["Profile"])

def main():
    """
    Entry point for running with: `poetry run start` (or similar).
    """
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
